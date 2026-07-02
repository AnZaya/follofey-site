#!/usr/bin/env python3
"""Upload bot avatar and configure"""
import urllib.request, json, os

TOKEN = "8763455476:AAGBsIIYXuAVGhKkflp24N_iOR0m-DrPQGQ"
AVATAR = "/Users/anzaya/follofey-site/assets/bot_avatar.png"

# Upload avatar
boundary = "----Boundary7MA4YW"
with open(AVATAR, 'rb') as f:
    img_data = f.read()

body = b"--" + boundary.encode() + b"\r\n"
body += b'Content-Disposition: form-data; name="photo"; filename="bot.png"\r\n'
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
    r = json.loads(resp.read())
    print(f"Photo: {r}")
except Exception as e:
    print(f"Photo error: {e}")

# Set commands (simple always works)
req2 = urllib.request.Request(
    f"https://api.telegram.org/bot{TOKEN}/setMyCommands",
    data=json.dumps({"commands": [
        {"command": "start", "description": "Приветствие"}
    ]}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
resp2 = urllib.request.urlopen(req2, timeout=10)
print(f"Commands: {json.loads(resp2.read())}")
