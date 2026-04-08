import json
import os
import torch
from flask import Flask, render_template, request, Response, stream_with_context
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from intents import INTENTS
from templates import generate_response

app = Flask(__name__)

MODEL_PATH = "intent_model"
_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model
    if os.path.exists(MODEL_PATH):
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()
        print("Intent model loaded.")
    else:
        print("WARNING: intent_model not found. Run python train_model.py first.")


def predict_intent(text: str) -> str:
    if _model is None or _tokenizer is None:
        return "out_of_scope"
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=32)
    with torch.no_grad():
        outputs = _model(**inputs)
    predicted = torch.argmax(outputs.logits).item()
    return INTENTS[predicted]


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

    intent = predict_intent(last_user_message)
    response = generate_response(intent, context=last_user_message)

    return Response(
        stream_with_context(stream_text(response)),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


load_model()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
