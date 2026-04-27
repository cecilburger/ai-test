"""
TikTok Live Comment Connector
Reads live_url from spaces.json, watches for changes, reconnects automatically.
"""

import asyncio
import aiohttp
import json
import os
import re
import time
import threading

CHATBOT_URL = os.environ.get("CHATBOT_URL", "http://127.0.0.1:5100/ailivechat/live_comment")
SPACES_FILE = os.path.join(os.path.dirname(__file__), "spaces.json")

def resolve_tiktok_username(url):
    """Extract @username from TikTok URL, following redirects for short URLs."""
    if not url:
        return None
    # Direct @username in URL
    m = re.search(r"tiktok\.com/@([^/?#]+)", url)
    if m:
        return m.group(1)
    # Short URL — follow redirect
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        final_url = resp.url
        m = re.search(r"tiktok\.com/@([^/?#]+)", final_url)
        if m:
            return m.group(1)
    except Exception as e:
        print(f"[Connector] Could not resolve URL {url}: {e}")
    return None

def get_username_from_spaces():
    """Read live_url from spaces.json and extract TikTok username."""
    if not os.path.exists(SPACES_FILE):
        return None
    try:
        with open(SPACES_FILE) as f:
            spaces = json.load(f)
        for sp in spaces.values():
            url = sp.get("live_url", "")
            if "tiktok.com" in url or "vt.tiktok.com" in url:
                username = resolve_tiktok_username(url)
                if username:
                    return username
    except Exception as e:
        print(f"[Connector] Error reading spaces.json: {e}")
    return None

def get_spaces_mtime():
    try:
        return os.path.getmtime(SPACES_FILE)
    except:
        return 0

async def run_connector(username):
    from TikTokLive import TikTokLiveClient
    from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent

    print(f"[Connector] Connecting to @{username}...")
    client = TikTokLiveClient(unique_id=username)

    @client.on(ConnectEvent)
    async def on_connect(event):
        print(f"[Connector] Connected to @{username} live!")

    @client.on(DisconnectEvent)
    async def on_disconnect(event):
        print(f"[Connector] Disconnected from @{username}.")

    @client.on(CommentEvent)
    async def on_comment(event):
        try:
            user_info = event.user_info
            uname = (
                getattr(user_info, "nick_name", None) or
                getattr(user_info, "unique_id", None) or
                "Kak"
            )
        except:
            uname = "Kak"
        comment = event.comment.strip()
        if not comment:
            return
        print(f"[{uname}]: {comment}")
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(CHATBOT_URL, json={"username": uname, "text": comment})
        except Exception as e:
            print(f"[Connector] Failed to forward: {e}")

    try:
        await client.start()
    except Exception as e:
        print(f"[Connector] Error: {e}")

def watch_and_run():
    last_username = None
    last_mtime = 0
    loop = None
    task = None

    while True:
        mtime = get_spaces_mtime()
        if mtime != last_mtime:
            last_mtime = mtime
            username = get_username_from_spaces()
            if not username:
                username = os.environ.get("TIKTOK_USERNAME", "skintific.official.store")

            if username != last_username:
                print(f"[Connector] Username changed: {last_username} → {username}")
                last_username = username

                # Stop old loop
                if loop and not loop.is_closed():
                    loop.call_soon_threadsafe(loop.stop)
                    time.sleep(2)

                # Start new loop
                loop = asyncio.new_event_loop()
                t = threading.Thread(target=lambda: loop.run_until_complete(run_connector(username)), daemon=True)
                t.start()

        time.sleep(5)  # check every 5 seconds

if __name__ == "__main__":
    print(f"[Connector] Starting — watching {SPACES_FILE}")
    print(f"[Connector] Forwarding to {CHATBOT_URL}")
    watch_and_run()
