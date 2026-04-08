import json
import re
from flask import Flask, render_template, request, Response, stream_with_context
from templates import generate_response, detect_intent

app = Flask(__name__)


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

    intent = detect_intent(last_user_message)
    response = generate_response(intent, context=last_user_message)

    return Response(
        stream_with_context(stream_text(response)),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
