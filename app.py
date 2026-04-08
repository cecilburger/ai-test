import json
import re
from flask import Flask, render_template, request, Response, stream_with_context
from qa_data import QA_DATA, OUT_OF_SCOPE

app = Flask(__name__)

MATCH_THRESHOLD = 2


def find_answer(user_message: str) -> str:
    text = user_message.lower()
    words = set(re.findall(r"\b\w+\b", text))

    best_match = None
    best_score = 0

    for entry in QA_DATA:
        score = sum(1 for kw in entry["keywords"] if kw in text or kw in words)
        if score > best_score:
            best_score = score
            best_match = entry

    if best_score >= MATCH_THRESHOLD:
        return best_match["answer"]

    # Single-keyword short entries (greetings, thanks)
    for entry in QA_DATA:
        for kw in entry["keywords"]:
            if kw in text and len(entry["keywords"]) <= 6:
                return entry["answer"]

    return OUT_OF_SCOPE


def stream_text(text: str):
    yield f"data: {json.dumps({'text': text})}\n\n"
    yield "data: [DONE]\n\n"


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

    answer = find_answer(last_user_message)

    return Response(
        stream_with_context(stream_text(answer)),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
