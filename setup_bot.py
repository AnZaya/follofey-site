#!/usr/bin/env python3
"""Setup FOLLOFEY bot and send test notification"""
import urllib.request, json, os

TOKEN = "8763455476:AAGBsIIYXuAVGhKkflp24N_iOR0m-DrPQGQ"
CHAT_ID = "512267849"
LOGO_PATH = "/Users/anzaya/follofey-site/assets/logo.png"

def tg_call(method, data, files=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if files:
        boundary = "----FormBoundary7MA4YWxkTrZu0gW"
        body = b""
        for k, v in files.items():
            with open(v, 'rb') as f:
                img = f.read()
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{os.path.basename(v)}\"\r\nContent-Type: image/png\r\n\r\n".encode()
            body += img + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    else:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}

# 1. Set photo
if os.path.exists(LOGO_PATH):
    r = tg_call("setMyPhoto", {}, files={"photo": LOGO_PATH})
    print(f"Photo: {r.get('ok')}")

# 2. Set description
r = tg_call("setMyDescription", {"description": "Бот для получения заявок с сайта follofey.ru. Уведомления о новых заказах и обращениях."})
print(f"Description: {r.get('ok')}")

# 3. Set short description
r = tg_call("setMyShortDescription", {"short_description": "Уведомления о заявках FOLLOFEY"})
print(f"About: {r.get('ok')}")

# 4. Set commands
r = tg_call("setMyCommands", {"commands": [{"command": "start", "description": "Приветствие"}]})
print(f"Commands: {r.get('ok')}")

# 5. Test notification
r = tg_call("sendMessage", {"chat_id": CHAT_ID, "text": "✅ Бот @FollofeyCampBot настроен и готов принимать заявки с сайта!"})
print(f"Test msg: {r.get('ok')}")

print("Done!")
