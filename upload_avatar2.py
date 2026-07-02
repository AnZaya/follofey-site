#!/usr/bin/env python3
"""Upload bot avatar using proper multipart"""
import urllib.request, json, os, io

TOKEN = "8763455476:AAGBsIIYXuAVGhKkflp24N_iOR0m-DrPQGQ"
AVATAR = "/Users/anzaya/follofey-site/assets/bot_avatar.png"
CHAT_ID = "512267849"

# Try uploading avatar via different approach
# Actually, let's just use python-telegram-bot if available
# Or try with the correct method name

# First - check what methods exist
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
r = urllib.request.urlopen(url, timeout=10)
print(f"Bot alive: {json.loads(r.read())}")

# Upload avatar using requests-style approach
with open(AVATAR, 'rb') as f:
    img_bytes = f.read()

# Telegram Bot API setMyPhoto: https://core.telegram.org/bots/api#setmyphoto
# Method exists since Bot API 6.7 (Telegram 9.0+)
# Let's check with explicit Content-Disposition

# Try using the exact format Telegram expects
# Actually, the issue might be that setMyPhoto doesn't exist in older Bot API
# Bot 7.0+ methods: setMyName, setMyDescription, setMyShortDescription, setMyPhoto, etc.

# Let's try a simpler approach - use setMyPhoto with a different boundary format
import http.client
import mimetypes

conn = http.client.HTTPSConnection("api.telegram.org")
boundary = "----WebKitFormBoundary" + os.urandom(12).hex()

# Build multipart body manually
body_parts = []
body_parts.append(f"--{boundary}\r\n".encode())
body_parts.append(b'Content-Disposition: form-data; name="photo"; filename="bot.png"\r\n')
body_parts.append(b"Content-Type: image/png\r\n\r\n")
body_parts.append(img_bytes)
body_parts.append(f"\r\n--{boundary}--\r\n".encode())
body = b"".join(body_parts)

conn.request(
    "POST",
    f"/bot{TOKEN}/setMyPhoto",
    body=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)

resp = conn.getresponse()
data = resp.read().decode()
print(f"Photo ({resp.status}): {data[:500]}")

# Also try to set description via setMyDescription
body2 = json.dumps({
    "description": "Бот для получения заявок с сайта follofey.ru. Уведомления о новых заказах и обращениях."
}).encode()
conn2 = http.client.HTTPSConnection("api.telegram.org")
conn2.request("POST", f"/bot{TOKEN}/setMyDescription", body=body2,
              headers={"Content-Type": "application/json"})
resp2 = conn2.getresponse()
print(f"Desc ({resp2.status}): {resp2.read().decode()[:200]}")

# Set short description  
body3 = json.dumps({
    "short_description": "🔔 Уведомления о заявках FOLLOFEY"
}).encode()
conn3 = http.client.HTTPSConnection("api.telegram.org")
conn3.request("POST", f"/bot{TOKEN}/setMyShortDescription", body=body3,
              headers={"Content-Type": "application/json"})
resp3 = conn3.getresponse()
print(f"About ({resp3.status}): {resp3.read().decode()[:200]}")

# Send message to my chat
body4 = json.dumps({
    "chat_id": CHAT_ID,
    "text": "✅ Бот @FollofeyCampBot настроен!\n\n📬 Теперь заявки с сайта будут приходить в этот чат."
}).encode()
conn4 = http.client.HTTPSConnection("api.telegram.org")
conn4.request("POST", f"/bot{TOKEN}/sendMessage", body=body4,
              headers={"Content-Type": "application/json"})
resp4 = conn4.getresponse()
print(f"Msg ({resp4.status}): {resp4.read().decode()[:300]}")
