import urllib.request, re

url = "https://vt.tiktok.com/ZS9NmMKC18n1E-Bvv8X/"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = urllib.request.urlopen(req, timeout=10)
    print("Final URL:", r.url)
    m = re.search(r"tiktok\.com/@([^/?#]+)", r.url)
    print("Username:", m.group(1) if m else "NOT FOUND")
except Exception as e:
    print("Error:", e)
