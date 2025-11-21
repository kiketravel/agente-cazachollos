import os
import requests

with open("resumen_chollos.txt", "r", encoding="utf-8") as f:
    mensaje = f.read()

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}

r = requests.post(url, data=data)
print("Respuesta Telegram:", r.text)
