"""
Video Worker — Wav2Lip lip sync engine
Replaces sadtalker_worker.py

Requirements:
    pip install flask opencv-python numpy

Wav2Lip setup:
    git clone https://github.com/Rudrabha/Wav2Lip.git
    cd Wav2Lip
    pip install -r requirements.txt
    # Download checkpoints:
    # wav2lip_gan.pth → Wav2Lip/checkpoints/wav2lip_gan.pth
    # Download from: https://github.com/Rudrabha/Wav2Lip#getting-the-weights

Usage:
    python video_worker.py
    (runs on port 5001, called by app.py /talk endpoint)
"""

import os
import sys
import uuid
import base64
import tempfile
import subprocess
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

WAV2LIP_DIR     = os.path.join(os.path.dirname(__file__), "Wav2Lip")
CHECKPOINT_PATH = os.path.join(WAV2LIP_DIR, "checkpoints", "wav2lip_gan.pth")
# Base idle video — record 5-10s of character looking natural, loop it
IDLE_VIDEO      = os.path.join(os.path.dirname(__file__), "static", "idle.mp4")
OUTPUT_DIR      = os.path.join(os.path.dirname(__file__), "static", "videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Video output queue for OBS
video_queue = []
video_queue_lock = threading.Lock()


def cleanup_old_videos(keep=5):
    """Keep only the N most recent videos to save disk space."""
    videos = sorted(
        [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")],
        key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)),
    )
    for old in videos[:-keep]:
        try:
            os.remove(os.path.join(OUTPUT_DIR, old))
        except Exception:
            pass


@app.route("/generate", methods=["POST"])
def generate():
    data      = request.get_json()
    audio_b64 = data.get("audio_b64", "")
    if not audio_b64:
        return jsonify({"error": "no audio"}), 400

    if not os.path.exists(IDLE_VIDEO):
        return jsonify({"error": f"idle.mp4 not found at {IDLE_VIDEO}"}), 500

    if not os.path.exists(CHECKPOINT_PATH):
        return jsonify({"error": f"Wav2Lip checkpoint not found at {CHECKPOINT_PATH}"}), 500

    # Save audio to temp wav file
    audio_bytes = base64.b64decode(audio_b64)
    audio_path  = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.wav")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    video_id   = str(uuid.uuid4())[:8]
    output_path = os.path.join(OUTPUT_DIR, f"talk_{video_id}.mp4")

    # Run Wav2Lip inference
    cmd = [
        sys.executable,
        os.path.join(WAV2LIP_DIR, "inference.py"),
        "--checkpoint_path", CHECKPOINT_PATH,
        "--face",            IDLE_VIDEO,
        "--audio",           audio_path,
        "--outfile",         output_path,
        "--pads",            "0", "10", "0", "0",
        "--resize_factor",   "1",
        "--nosmooth",
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=WAV2LIP_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            print(f"[Wav2Lip ERROR]\n{result.stderr}")
            return jsonify({"error": result.stderr[-500:]}), 500

        if not os.path.exists(output_path):
            return jsonify({"error": "output video not created"}), 500

        cleanup_old_videos()

        video_url = f"/static/videos/talk_{video_id}.mp4"

        # Add to OBS queue
        with video_queue_lock:
            video_queue.append(output_path)

        return jsonify({"video_url": video_url})

    except subprocess.TimeoutExpired:
        return jsonify({"error": "timeout after 120s"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


@app.route("/queue", methods=["GET"])
def get_queue():
    """OBS or external player polls this to get next video to play."""
    with video_queue_lock:
        if video_queue:
            next_video = video_queue.pop(0)
            return jsonify({"video": next_video, "remaining": len(video_queue)})
        return jsonify({"video": None, "remaining": 0})


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "wav2lip_ready": os.path.exists(CHECKPOINT_PATH),
        "idle_video_ready": os.path.exists(IDLE_VIDEO),
        "queue_length": len(video_queue),
        "output_dir": OUTPUT_DIR,
    })


if __name__ == "__main__":
    print("=" * 50)
    print("Video Worker (Wav2Lip) running on port 5001")
    print(f"Wav2Lip dir:   {WAV2LIP_DIR}")
    print(f"Checkpoint:    {CHECKPOINT_PATH} {'✓' if os.path.exists(CHECKPOINT_PATH) else '✗ MISSING'}")
    print(f"Idle video:    {IDLE_VIDEO} {'✓' if os.path.exists(IDLE_VIDEO) else '✗ MISSING'}")
    print("=" * 50)
    app.run(port=5001, debug=False)
