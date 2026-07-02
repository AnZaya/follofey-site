#!/usr/bin/env python3
"""FOLLOFEY — сервер приёма заявок с сайта и отправки в Telegram"""
import json, os, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import urllib.request

BOT_TOKEN = "8763455476:AAGBsIIYXuAVGhKkflp24N_iOR0m-DrPQGQ"
CHAT_ID = "512267849"
HOST = "0.0.0.0"
PORT = 8765

def send_tg(text):
    data = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except:
        return False

class FormHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        # Parse form data (JSON or URL-encoded)
        if self.headers.get("Content-Type", "").startswith("application/json"):
            data = json.loads(body)
        else:
            data = parse_qs(body)
            data = {k: v[0] if isinstance(v, list) else v for k, v in data.items()}

        name = data.get("name", data.get("Name", "Не указано"))
        email = data.get("email", data.get("Email", "Не указано"))
        phone = data.get("phone", data.get("Phone", "Не указано"))
        message = data.get("message", data.get("Message", data.get("text", "Не указано")))

        # Format notification
        tg_text = (
            f"🔔 <b>Новая заявка с сайта FOLLOFEY!</b>\n\n"
            f"👤 <b>Имя:</b> {name}\n"
            f"📧 <b>Email:</b> {email}\n"
            f"📞 <b>Телефон:</b> {phone}\n"
            f"💬 <b>Сообщение:</b> {message[:500]}"
        )

        ok = send_tg(tg_text)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        resp = json.dumps({"ok": ok, "message": "Заявка отправлена!"}, ensure_ascii=False)
        self.wfile.write(resp.encode("utf-8"))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"FOLLOFEY Form Server running\n")

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}", flush=True)

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), FormHandler)
    print(f"🚀 FOLLOFEY form server running on http://{HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()
