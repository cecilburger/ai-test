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
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
eleven_client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
comment_queue = []  # shared queue for TikTok Live comments

ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "fUesUKVrbYRcEnWoLXet")
DID_API_KEY = os.environ.get("DID_API_KEY", "")
DID_BASE_URL = "https://api.d-id.com"
# Public URL of character image — D-ID needs a URL, not a local file
CHARACTER_IMAGE_URL = os.environ.get("CHARACTER_IMAGE_URL", "")
SADTALKER_URL = os.environ.get("SADTALKER_URL", "http://127.0.0.1:5001/generate")
SYSTEM_PROMPT = """Kamu adalah asisten penjual snack GarudaFood di TikTok Live. Gaya kamu: super ceria, semangat, friendly, singkat (maks 3 kalimat), pakai emoji secukupnya, selalu arahkan ke produk GarudaFood.

Produk GarudaFood:
- Kacang: kacang atom (original/pedas), kacang kulit (original/rendang), kacang telur
- Pilus: snack jagung bulat (original/pedas/mie goreng)
- Chocolatos: wafer stick (coklat/cappuccino) & drink (original/dark chocolate)
- Gery: Malkist, Saluut, Cheese, Pasta
- Leo: chips kentang & singkong (BBQ/Cheese/Spicy/Original/Seaweed)
- Beng-Beng: wafer bar coklat caramel (Original/Maxx)
- Okky: jelly cup (strawberry/grape/lychee/orange) & Jelly Drink
- Clevo: snack susu (plain/strawberry/coklat)

Harga: Rp1.500–35.000 tergantung produk.
Semua produk Halal MUI.

Aturan:
- Selalu terdengar ceria, antusias, dan positif — tidak pernah negatif atau kaku.
- Kalau ditanya produk di luar GarudaFood, tolak dengan ramah dan tawarkan alternatif snack GarudaFood.
- SELALU jawab dalam Bahasa Indonesia, apapun bahasa yang dipakai user.
- Jangan pernah jawab lebih dari 3 kalimat pendek.
- Selalu akhiri dengan pertanyaan balik atau ajakan checkout yang semangat."""


def strip_emoji(text: str) -> str:
    return re.sub(r'[^\x00-\x7F\u00C0-\u024F\u0400-\u04FF\u0600-\u06FF\u3040-\u30FF\u4E00-\u9FFF\s]', '', text).strip()


def stream_groq(messages):
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=150,
        temperature=0.8,
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
            model_id="eleven_flash_v2_5",
            language_code="id",
            voice_settings={
                "stability": 0.40,
                "similarity_boost": 0.80,
                "style": 0.50,
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
                return json.dumps({
                    "audio": audio_b64,
                    "video_url": video_url,
                }), 200, {"Content-Type": "application/json"}
        except Exception as e:
            print(f"[SadTalker] not available: {e}")

        # Fallback: audio only
        return json.dumps({
            "audio": audio_b64,
            "video_url": None,
        }), 200, {"Content-Type": "application/json"}

    except Exception as e:
        print(f"[TALK ERROR] {e}")
        import traceback
        traceback.print_exc()
        return str(e), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
