"""
Intent detection — minimal, universal (no product-specific rules)
Used only to pass a context hint to the LLM.
"""

import re

RULES = [
    ("greeting",    r"\b(halo|hai|hello|hi|hey|selamat pagi|selamat siang|selamat sore|selamat malam)\b"),
    ("thanks",      r"\b(makasih|terima kasih|thanks|thank you|thx)\b"),
    ("question",    r"\?"),
]


def detect_intent(text: str) -> str:
    t = text.lower()
    for intent, pattern in RULES:
        if re.search(pattern, t):
            return intent
    return "general"


INTENT_CONTEXT = {
    "greeting": "User menyapa, balas dengan ramah dan ceria.",
    "thanks":   "User berterima kasih, balas dengan hangat.",
    "question": "User bertanya sesuatu, jawab dengan informatif dan menarik.",
    "general":  "User mengirim pesan, respon dengan natural dan engaging.",
}
