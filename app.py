import json
import os
import re
import base64
import requests as http_requests
from flask import Flask, render_template, request, Response, stream_with_context, send_from_directory
from groq import Groq
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from templates import detect_intent, INTENT_CONTEXT

load_dotenv()

app = Flask(__name__)
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
eleven_client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
comment_queue = []  # shared queue for TikTok Live comments
bot_audio_queue = []  # audio pushed to OBS view

ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "fUesUKVrbYRcEnWoLXet")
DID_API_KEY = os.environ.get("DID_API_KEY", "")
DID_BASE_URL = "https://api.d-id.com"
# Public URL of character image — D-ID needs a URL, not a local file
CHARACTER_IMAGE_URL = os.environ.get("CHARACTER_IMAGE_URL", "")
SADTALKER_URL = os.environ.get("SADTALKER_URL", "http://127.0.0.1:5001/generate")
SYSTEM_PROMPT = """Kamu adalah Meili, host live streaming yang ramah dan ceria untuk produk Tepung Super. Kamu adalah manusia, bukan AI.

Jika ditanya apakah kamu AI, robot, atau bot: jawab "Aku Meili, host live ini 😊" — jangan pernah mengaku sebagai AI.

Kamu HANYA menjawab pertanyaan seputar produk Tepung Super. Berikut pengetahuanmu:

=== PRODUK TEPUNG SUPER ===

Bumbu inti fried chicken Tepung Super terdiri dari 2 produk utama:

--- PREMIX BIANG 1801 ---
- Nama produk: Bumbu Biang / Premix 1801
- Rasio pemakaian: 1 kg biang dicampur 5 kg tepung terigu (perbandingan 1:5)
- Contoh: 200 gr biang + 1 kg tepung terigu
- Hasil campuran 6 kg bisa untuk penepungan 10–12 ekor ayam
- Cara pakai: Campurkan biang dan terigu, aduk rata 5–10 menit hingga benar-benar tercampur, lalu siap digunakan untuk penepungan ayam

--- MARINADE 1802 ---
- Nama produk: Bumbu Marinade 1802
- Takaran: 20 gr per 1 ekor ayam (1 sendok makan)
- 1 kg marinade cukup untuk 50 ekor ayam (50 kg)
- Cara pakai: Larutkan 20 gr marinade ke dalam 80 cc air, aduk hingga larut, tuang ke potongan ayam bersih, aduk rata hingga bumbu menyusut dan terserap ke dalam daging

=== CARA PENGGUNAAN TEPUNG BIANG 1801 ===
1. Campurkan 200 gr Tepung Biang dengan 1 kg Tepung Terigu (Segitiga atau merek lainnya)
2. Aduk sampai tercampur rata
3. Tepung siap digunakan untuk penepungan ayam

=== PEMESANAN & PENGIRIMAN ===
- Pesan sebelum jam 17.30 → dikirim hari yang sama
- Hari Minggu: pesan sebelum jam 16.00 → dikirim hari yang sama

=== PENYIMPANAN ===
- Stok selalu baru, tahan hingga 6 bulan
- Simpan di tempat sejuk, bersih, dan kering
- Rapatkan tutup setelah dibuka
- Hindari sinar matahari langsung
- Hindari percikan air dan bahan berbau

=== INFORMASI UMUM PRODUK ===
- Produk: Premix Biang 1801 dan Marinade 1802
- Fungsi: Bumbu fried chicken crispy
- Hasil: Ayam crispy, gurih, golden, renyah tahan lama
- Cocok untuk: Usaha fried chicken, rumahan, UMKM, restoran, catering, frozen food
- Halal: Ya
- Tanda rusak: Bau atau menggumpal

Aturan:
- SELALU jawab dalam Bahasa Indonesia
- Jawaban singkat dan natural seperti orang live
- Sapaan → balas singkat: "Halo [nama]!" dll
- Jika pertanyaan di luar topik produk Tepung Super → jawab: "Maaf, aku cuma bisa bantu soal produk Tepung Super ya kak 😊"
- JANGAN pernah mengaku sebagai AI"""


def strip_emoji(text: str) -> str:
    return re.sub(r'[^\x00-\x7F\u00C0-\u024F\u0400-\u04FF\u0600-\u06FF\u3040-\u30FF\u4E00-\u9FFF\s]', '', text).strip()


def stream_groq(messages):
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=150,
        temperature=0.7,
        stream=True,
    )
    for chunk in completion:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'text': delta})}\n\n"
    yield "data: [DONE]\n\n"


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/obs")
def obs():
    return render_template("obs.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    last_user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_message = m.get("content", "")
            break

    intent = detect_intent(last_user_message)
    context_hint = INTENT_CONTEXT.get(intent, "")
    system = SYSTEM_PROMPT
    if context_hint:
        system += f"\n\nKonteks pertanyaan ini: {context_hint}"

    groq_messages = [{"role": "system", "content": system}] + [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m.get("role") in ("user", "assistant")
    ]

    return Response(
        stream_with_context(stream_groq(groq_messages)),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/live_comment", methods=["POST"])
def live_comment():
    """Receives comments from TikTok Live connector and pushes to frontend via SSE."""
    data = request.get_json()
    username = data.get("username", "Kak")
    text = data.get("text", "").strip()
    if not text:
        return "", 400
    comment_queue.append({"username": username, "text": text})
    return "", 200


@app.route("/live_stream")
def live_stream():
    """SSE endpoint — frontend subscribes to get live comments pushed in real-time."""
    def event_stream():
        last = 0
        while True:
            if len(comment_queue) > last:
                item = comment_queue[last]
                last += 1
                import json as _json
                yield f"data: {_json.dumps(item)}\n\n"
            else:
                import time
                time.sleep(0.3)
    return Response(stream_with_context(event_stream()),
                    mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = strip_emoji(data.get("text", ""))
    if not text:
        return "", 400

    try:
        # Use convert_with_timestamps to get alignment data for lip sync
        response = eleven_client.text_to_speech.convert_with_timestamps(
            voice_id=ELEVENLABS_VOICE_ID,
            text=text,
            model_id="eleven_flash_v2_5",
            language_code="id",
            voice_settings={
                "stability": 0.40,
                "similarity_boost": 0.80,
                "style": 0.50,
                "use_speaker_boost": True,
            },
        )

        # Response structure: audio_bytes (bytes) and alignment dict
        audio_b64 = response.audio_base_64 or ""

        # Build viseme timeline from character alignment
        visemes = []
        if hasattr(response, 'alignment') and response.alignment:
            alignment = response.alignment
            chars  = getattr(alignment, 'characters', []) or []
            starts = getattr(alignment, 'character_start_times_seconds', []) or []
            ends   = getattr(alignment, 'character_end_times_seconds', []) or []
            for ch, st, en in zip(chars, starts, ends):
                visemes.append({"char": ch, "start": st, "end": en})

        return json.dumps({
            "audio": audio_b64,
            "visemes": visemes,
        }), 200, {"Content-Type": "application/json"}

    except Exception as e:
        print(f"[TTS ERROR] {e}")
        import traceback
        traceback.print_exc()
        return str(e), 500


@app.route("/talk", methods=["POST"])
def talk():
    """Generate SadTalker talking head video from text."""
    data = request.get_json()
    text = strip_emoji(data.get("text", ""))
    if not text:
        return json.dumps({"error": "missing text"}), 400

    try:
        # Step 1: Get audio from ElevenLabs
        eleven_response = eleven_client.text_to_speech.convert_with_timestamps(
            voice_id=ELEVENLABS_VOICE_ID,
            text=text,
            model_id="eleven_v3",
            language_code="id",
            voice_settings={
                "stability": 0.30,
                "similarity_boost": 0.80,
                "style": 0.65,
                "use_speaker_boost": True,
            },
        )
        audio_b64 = eleven_response.audio_base_64 or ""

        # Step 2: Send to SadTalker worker
        try:
            st_res = http_requests.post(
                SADTALKER_URL,
                json={"audio_b64": audio_b64},
                timeout=120,
            )
            if st_res.ok:
                video_url = st_res.json().get("video_url")
                result = json.dumps({"audio": audio_b64, "video_url": video_url})
                bot_audio_queue.append({"audio": audio_b64, "video_url": video_url})
                return result, 200, {"Content-Type": "application/json"}
        except Exception as e:
            print(f"[SadTalker] not available: {e}")

        # Fallback: audio only
        result = json.dumps({
            "audio": audio_b64,
            "video_url": None,
        })
        bot_audio_queue.append({"audio": audio_b64, "video_url": None})
        return result, 200, {"Content-Type": "application/json"}

    except Exception as e:
        print(f"[TALK ERROR] {e}")
        import traceback
        traceback.print_exc()
        return json.dumps({"audio": None, "video_url": None}), 200, {"Content-Type": "application/json"}


@app.route("/bot_stream")
def bot_stream():
    """SSE — OBS view subscribes to get audio/video pushed when bot speaks."""
    def event_stream():
        last = 0
        while True:
            if len(bot_audio_queue) > last:
                item = bot_audio_queue[last]
                last += 1
                yield f"data: {json.dumps(item)}\n\n"
            else:
                import time
                time.sleep(0.3)
    return Response(stream_with_context(event_stream()),
                    mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Admin credentials ─────────────────────────────────────────────────────────
ADMIN_USER = "mrhan"
ADMIN_PASS = "mcnasia"

# ── Spaces storage (in-memory, persisted to spaces.json) ──────────────────────
SPACES_FILE = os.path.join(os.path.dirname(__file__), "spaces.json")

def load_spaces():
    if os.path.exists(SPACES_FILE):
        with open(SPACES_FILE) as f:
            return json.load(f)
    # default space
    return {"default": {"name": "Default", "video_url": "", "live_url": "", "knowledge": ""}}

def save_spaces(spaces):
    with open(SPACES_FILE, "w") as f:
        json.dump(spaces, f, indent=2)

@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    if data.get("username") == ADMIN_USER and data.get("password") == ADMIN_PASS:
        return json.dumps({"ok": True}), 200, {"Content-Type": "application/json"}
    return json.dumps({"ok": False}), 401, {"Content-Type": "application/json"}

@app.route("/admin/spaces", methods=["GET"])
def get_spaces():
    return json.dumps(load_spaces()), 200, {"Content-Type": "application/json"}

@app.route("/admin/spaces", methods=["POST"])
def create_space():
    data = request.get_json()
    if data.get("username") != ADMIN_USER or data.get("password") != ADMIN_PASS:
        return "", 401
    spaces = load_spaces()
    sid = re.sub(r"[^a-z0-9_]", "_", data["name"].lower().strip())
    if not sid:
        return json.dumps({"error": "invalid name"}), 400, {"Content-Type": "application/json"}
    spaces[sid] = {"name": data["name"], "video_url": "", "live_url": "", "knowledge": ""}
    save_spaces(spaces)
    return json.dumps({"ok": True, "id": sid}), 200, {"Content-Type": "application/json"}

@app.route("/admin/spaces/<sid>", methods=["PUT"])
def update_space(sid):
    data = request.get_json()
    if data.get("username") != ADMIN_USER or data.get("password") != ADMIN_PASS:
        return "", 401
    spaces = load_spaces()
    if sid not in spaces:
        return "", 404
    for key in ("video_url", "live_url", "knowledge", "name"):
        if key in data:
            spaces[sid][key] = data[key]
    save_spaces(spaces)
    return json.dumps({"ok": True}), 200, {"Content-Type": "application/json"}

@app.route("/admin/spaces/<sid>", methods=["DELETE"])
def delete_space(sid):
    data = request.get_json()
    if data.get("username") != ADMIN_USER or data.get("password") != ADMIN_PASS:
        return "", 401
    spaces = load_spaces()
    if sid == "default":
        return json.dumps({"error": "cannot delete default"}), 400, {"Content-Type": "application/json"}
    spaces.pop(sid, None)
    save_spaces(spaces)
    return json.dumps({"ok": True}), 200, {"Content-Type": "application/json"}


SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "static", "sounds")
os.makedirs(SOUNDS_DIR, exist_ok=True)

@app.route("/admin/spaces/<sid>/sounds", methods=["GET"])
def get_sounds(sid):
    folder = os.path.join(SOUNDS_DIR, sid)
    if not os.path.exists(folder):
        return json.dumps([]), 200, {"Content-Type": "application/json"}
    files = sorted([f for f in os.listdir(folder) if f.endswith(".mp3")])
    return json.dumps(files), 200, {"Content-Type": "application/json"}

@app.route("/admin/spaces/<sid>/upload_sound", methods=["POST"])
def upload_sound(sid):
    username = request.form.get("username")
    password = request.form.get("password")
    if username != ADMIN_USER or password != ADMIN_PASS:
        return "", 401
    folder = os.path.join(SOUNDS_DIR, sid)
    os.makedirs(folder, exist_ok=True)
    existing = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    if len(existing) >= 10:
        return json.dumps({"error": "Max 10 sounds per space"}), 400, {"Content-Type": "application/json"}
    f = request.files.get("file")
    if not f or not f.filename.endswith(".mp3"):
        return json.dumps({"error": "MP3 only"}), 400, {"Content-Type": "application/json"}
    safe_name = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", f.filename)
    f.save(os.path.join(folder, safe_name))
    return json.dumps({"ok": True, "filename": safe_name}), 200, {"Content-Type": "application/json"}

@app.route("/admin/spaces/<sid>/delete_sound", methods=["POST"])
def delete_sound(sid):
    data = request.get_json()
    if data.get("username") != ADMIN_USER or data.get("password") != ADMIN_PASS:
        return "", 401
    filename = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", data.get("filename", ""))
    path = os.path.join(SOUNDS_DIR, sid, filename)
    if os.path.exists(path):
        os.remove(path)
    return json.dumps({"ok": True}), 200, {"Content-Type": "application/json"}

@app.route("/static/sounds/<sid>/<filename>")
def serve_sound(sid, filename):
    folder = os.path.join(SOUNDS_DIR, sid)
    return send_from_directory(folder, filename)

@app.route("/chat/space/<sid>", methods=["POST"])
def chat_space(sid):
    """Chat endpoint that uses space-specific knowledge as system prompt."""
    spaces = load_spaces()
    space = spaces.get(sid, spaces.get("default", {}))
    knowledge = space.get("knowledge", "").strip()

    data = request.get_json()
    messages = data.get("messages", [])

    last_user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_message = m.get("content", "")
            break

    intent = detect_intent(last_user_message)
    context_hint = INTENT_CONTEXT.get(intent, "")

    if knowledge:
        system = f"""Kamu adalah Meili, host live streaming yang ramah dan ceria. Kamu adalah manusia, bukan AI.
Jika ditanya apakah kamu AI, robot, atau bot: jawab "Aku Meili, host live ini 😊" — jangan pernah mengaku sebagai AI.
Kamu HANYA menjawab pertanyaan seputar topik berikut:

{knowledge}

Aturan:
- SELALU jawab dalam Bahasa Indonesia
- Jawaban singkat dan natural seperti orang live
- Jika pertanyaan di luar topik → jawab: "Maaf, aku cuma bisa bantu soal topik ini ya kak 😊"
- JANGAN pernah mengaku sebagai AI"""
    else:
        system = SYSTEM_PROMPT

    if context_hint:
        system += f"\n\nKonteks: {context_hint}"

    groq_messages = [{"role": "system", "content": system}] + [
        {"role": m["role"], "content": m["content"]}
        for m in messages if m.get("role") in ("user", "assistant")
    ]

    return Response(
        stream_with_context(stream_groq(groq_messages)),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
