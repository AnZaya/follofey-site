#!/usr/bin/env python3
import urllib.request, json

TOKEN = "8763455476:AAGBsIIYXuAVGhKkflp24N_iOR0m-DrPQGQ"

# Check getMe
r = urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=10)
info = json.loads(r.read())
print(f"Bot: {info['result']['username']} - {info['result']['first_name']}")

# Check file size
import os
logo = "assets/logo.png"
if os.path.exists(logo):
    sz = os.path.getsize(logo)
    print(f"Logo size: {sz} bytes ({sz/1024:.0f} KB)")
    if sz > 51200:
        print("Too large! Telegram max is 50KB for photo")

# Try upload with correct boundary
import http.client
boundary = "----FormBoundary7MA4YWxkTrZu0gW"
with open(logo, 'rb') as f:
    img_data = f.read()

body = b"--" + boundary.encode() + b"\r\n"
body += b'Content-Disposition: form-data; name="photo"; filename="logo.png"\r\n'
body += b"Content-Type: image/png\r\n\r\n"
body += img_data
body += b"\r\n--" + boundary.encode() + b"--\r\n"

req = urllib.request.Request(
    f"https://api.telegram.org/bot{TOKEN}/setMyPhoto",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST"
)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    r2 = json.loads(resp.read())
    print(f"Photo upload: {r2}")
except Exception as e:
    print(f"Photo error: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode()[:500])

# Check updates for chat
r3 = urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/getUpdates", timeout=10)
upd = json.loads(r3.read())
print(f"Updates count: {len(upd.get('result', []))}")
for u in upd.get('result', []):
    msg = u.get('message', {})
    chat = msg.get('chat', {})
    print(f"  Chat: {chat.get('id')} ({chat.get('type')}) - {chat.get('username', 'no username')}")
