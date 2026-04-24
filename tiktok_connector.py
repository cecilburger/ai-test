"""
TikTok Live Comment Connector
Connects to a TikTok Live stream and forwards comments to the chatbot via HTTP.

Reads TIKTOK_USERNAME from env or spaces.json (live_url field).
Usage:
    python tiktok_connector.py
"""

import asyncio
import aiohttp
import json
import os
import re
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent

CHATBOT_URL = os.environ.get("CHATBOT_URL", "http://127.0.0.1:5100/ailivechat/live_comment")

def get_username_from_spaces():
    """Read live_url from spaces.json and extract TikTok username."""
    spaces_file = os.path.join(os.path.dirname(__file__), "spaces.json")
    if os.path.exists(spaces_file):
        with open(spaces_file) as f:
            spaces = json.load(f)
        for sp in spaces.values():
            url = sp.get("live_url", "")
            if "tiktok.com" in url:
                m = re.search(r"tiktok\.com/@([^/?#]+)", url)
                if m:
                    return m.group(1)
    return None

TIKTOK_USERNAME = (
    os.environ.get("TIKTOK_USERNAME") or
    get_username_from_spaces() or
    "skintific.official.store"
)

print(f"Target: @{TIKTOK_USERNAME}")
print(f"Forwarding to: {CHATBOT_URL}")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{TIKTOK_USERNAME} live!")

@client.on(DisconnectEvent)
async def on_disconnect(event: DisconnectEvent):
    print("Disconnected from live.")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    try:
        user_info = event.user_info
        username = (
            getattr(user_info, "nick_name", None) or
            getattr(user_info, "unique_id", None) or
            "Kak"
        )
    except Exception:
        username = "Kak"

    comment = event.comment.strip()
    if not comment:
        return

    print(f"[{username}]: {comment}")

    try:
        async with aiohttp.ClientSession() as session:
            await session.post(CHATBOT_URL, json={"username": username, "text": comment})
    except Exception as e:
        print(f"Failed to forward comment: {e}")

if __name__ == "__main__":
    print(f"Connecting to @{TIKTOK_USERNAME} live...")
    client.run()
