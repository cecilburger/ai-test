"""
SadTalker worker — generates talking head video from image + audio.
Run this alongside app.py.

Requirements:
    - SadTalker cloned at ./SadTalker/
    - Model weights downloaded in ./SadTalker/checkpoints/
    - pip install flask requests

Usage:
    python sadtalker_worker.py
"""

import os
import sys
import uuid
import base64
import tempfile
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

SADTALKER_DIR = os.path.join(os.path.dirname(__file__), "SadTalker")
CHARACTER_IMG = os.path.join(os.path.dirname(__file__), "static", "character.png")
OUTPUT_DIR    = os.path.join(os.path.dirname(__file__), "static", "videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    audio_b64 = data.get("audio_b64", "")
    if not audio_b64:
        return jsonify({"error": "no audio"}), 400

    # Save audio to temp file
    audio_bytes = base64.b64decode(audio_b64)
    audio_path  = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.wav")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    # Output video path
    video_id   = str(uuid.uuid4())
    video_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")

    # Run SadTalker
    cmd = [
        sys.executable,
        os.path.join(SADTALKER_DIR, "inference.py"),
        "--driven_audio", audio_path,
        "--source_image", CHARACTER_IMG,
        "--result_dir", OUTPUT_DIR,
        "--still",           # less head movement, more natural for live host
        "--preprocess", "full",
        "--enhancer", "gfpgan",  # face enhancement for better quality
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=SADTALKER_DIR,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"[SadTalker ERROR] {result.stderr}")
            return jsonify({"error": result.stderr}), 500

        # Find generated video (SadTalker saves with timestamp in name)
        videos = sorted(
            [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")],
            key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)),
            reverse=True,
        )
        if not videos:
            return jsonify({"error": "no video generated"}), 500

        latest_video = videos[0]
        video_url    = f"/static/videos/{latest_video}"
        return jsonify({"video_url": video_url})

    except subprocess.TimeoutExpired:
        return jsonify({"error": "timeout"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    print("SadTalker worker running on port 5001")
    app.run(port=5001, debug=False)
