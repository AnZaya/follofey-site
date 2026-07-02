#!/usr/bin/env python3
"""Check bot status and try to send test message"""
import urllib.request, json

TOKEN = "8763455476:AAGBsIIYXuAVGhKkflp24N_iOR0m-DrPQGQ"
CHAT_ID = "512267849"

# 1. Check updates (user pressed /start)
req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/getUpdates", method="GET")
resp = urllib.request.urlopen(req, timeout=10)
upd = json.loads(resp.read())
print(f"Updates: {json.dumps(upd, indent=2, ensure_ascii=False)[:1000]}")
print(f"Total updates: {len(upd.get('result', []))}")

if upd.get('result'):
    u = upd['result'][-1]
    chat = u.get('message', {}).get('chat', {})
    print(f"Last chat: id={chat.get('id')} type={chat.get('type')} username={chat.get('username')}")

# 2. Try send a test message
body = json.dumps({
    "chat_id": CHAT_ID,
    "text": "✅ Бот @FollofeyCampBot подключён! Теперь заявки с сайта будут приходить сюда.",
    "parse_mode": "HTML"
}).encode()
req2 = urllib.request.Request(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data=body, headers={"Content-Type": "application/json"}, method="POST"
)
resp2 = urllib.request.urlopen(req2, timeout=10)
print(f"Send test: {json.loads(resp2.read())}")
