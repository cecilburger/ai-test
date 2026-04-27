"""
TikTok Live Comment Connector
Reads ALL live_url values from spaces.json, connects to each TikTok live.
Restarts automatically if spaces.json changes.
"""

import asyncio
import aiohttp
import json
import os
import re
import urllib.request

CHATBOT_URL = os.environ.get("CHATBOT_URL", "http://127.0.0.1:5100/ailivechat/live_comment")
SPACES_FILE = os.path.join(os.path.dirname(__file__), "spaces.json")


def resolve_tiktok_username(url):
    if not url:
        return None
    # Direct @username
    m = re.search(r"tiktok\.com/@([^/?#\n]+)", url)
    if m:
        return m.group(1).strip()
    # Short URL — follow redirect
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        final = resp.url
        print(f"[Connector] Resolved {url} → {final}")
        m = re.search(r"tiktok\.com/@([^/?#\n]+)", final)
        if m:
            return m.group(1).strip()
    except Exception as e:
        print(f"[Connector] Could not resolve {url}: {e}")
    return None


def get_all_usernames():
    usernames = set()
    try:
        with open(SPACES_FILE) as f:
            spaces = json.load(f)
        for sp in spaces.values():
            url = sp.get("live_url", "").strip()
            if "tiktok" in url:
                u = resolve_tiktok_username(url)
                if u:
                    usernames.add(u)
    except Exception as e:
        print(f"[Connector] Error reading spaces.json: {e}")
    return usernames


async def connect_to(username):
    from TikTokLive import TikTokLiveClient
    from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent

    while True:
        print(f"[Connector] Connecting to @{username}...")
        client = TikTokLiveClient(unique_id=username)

        @client.on(ConnectEvent)
        async def on_connect(event):
            print(f"[Connector] ✅ Connected to @{username}")

        @client.on(DisconnectEvent)
        async def on_disconnect(event):
            print(f"[Connector] ❌ Disconnected from @{username}")

        @client.on(CommentEvent)
        async def on_comment(event):
            try:
                ui = event.user_info
                uname = getattr(ui, "nick_name", None) or getattr(ui, "unique_id", None) or "Kak"
            except:
                uname = "Kak"
            comment = event.comment.strip()
            if not comment:
                return
            print(f"[@{username}] [{uname}]: {comment}")
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(CHATBOT_URL, json={"username": uname, "text": comment}, timeout=aiohttp.ClientTimeout(total=5))
            except Exception as e:
                print(f"[Connector] Forward error: {e}")

        try:
            await client.start()
        except Exception as e:
            print(f"[Connector] @{username} not live or error: {e}. Retrying in 30s...")

        await asyncio.sleep(30)  # wait before retrying


async def main():
    usernames = get_all_usernames()
    if not usernames:
        fallback = os.environ.get("TIKTOK_USERNAME", "skintific.official.store")
        print(f"[Connector] No TikTok URLs in spaces.json, using fallback: @{fallback}")
        usernames = {fallback}

    print(f"[Connector] Connecting to: {usernames}")
    tasks = [asyncio.create_task(connect_to(u)) for u in usernames]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print(f"[Connector] Starting...")
    print(f"[Connector] Forwarding to: {CHATBOT_URL}")
    asyncio.run(main())
