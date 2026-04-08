import os
import json
import re
from flask import Flask, render_template, request, Response, stream_with_context
import anthropic
from dotenv import load_dotenv
from qa_data import QA_DATA

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a friendly and knowledgeable customer service chatbot for Garuda Food, a leading Indonesian snack food company. Your sole purpose is to help customers with questions about Garuda Food's snack products.

You can help with:
- Product information: ingredients, flavors, sizes, and packaging
- Nutritional details and allergen information
- Product recommendations based on preferences
- Where to find or buy Garuda Food products
- Garuda Food's snack brands and product lines
- Promotions or general brand information

Garuda Food's key snack products and brands include:
- Kacang Garuda – roasted peanuts in flavors like original, spicy, and coated varieties
- Chocolatos – chocolate-flavored wafer sticks, a popular snack for kids and adults
- Gery – a wide range of biscuits, wafers, and cookies
- Okky – jelly snacks and drinks in fun flavors
- Leo – chips, crackers, and savory snacks
- Beng-Beng – chocolate wafer bars with caramel
- Clevo – milk-based snack products

If a user asks about anything NOT related to Garuda Food snack products (e.g., competitors, unrelated topics, personal advice, news, etc.), politely decline and redirect them. Say something like: "I'm only able to help with questions about Garuda Food snack products. Is there anything about our products I can help you with?"

Keep answers concise and helpful. Be warm and conversational."""

# Minimum keyword matches required to use a cached answer
MATCH_THRESHOLD = 2


def find_cached_answer(user_message: str) -> str | None:
    """Return a cached answer if the message matches a known Q&A entry."""
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

    # Single-keyword entries (greetings, thanks) only need 1 match
    for entry in QA_DATA:
        for kw in entry["keywords"]:
            if kw in text and len(entry["keywords"]) <= 6:
                return entry["answer"]

    return None


def stream_text(text: str):
    """Yield a static text as a single SSE chunk (instant, no API call)."""
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

    cached = find_cached_answer(last_user_message)

    if cached:
        # Instant response from local data — no API call
        return Response(
            stream_with_context(stream_text(cached)),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    # Fallback to Claude for questions not covered by cached data
    def generate_from_api():
        with client.messages.stream(
            model="claude-haiku-4-5",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate_from_api()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
