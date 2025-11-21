# enviar_telegram.py
import os
import requests
import textwrap
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Faltan TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en los secrets.")
    exit(1)

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
CATEGORIES = [
    ("vuelos", "✈️ TOP 10 VUELOS"),
    ("vuelo_hotel", "🏖️ TOP 10 VUELO+HOTEL"),
    ("hoteles", "🏨 TOP 10 HOTELES"),
    ("paquetes", "🌍 TOP 10 PAQUETES")
]

MAX_LEN = 3800  # dejar margen para Markdown

def send_message(text):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(BASE_URL, json=payload, timeout=15)
        print("Telegram response:", r.status_code, r.text)
        return r.status_code == 200
    except Exception as e:
        print("Error enviando a Telegram:", e)
        return False

for key, title in CATEGORIES:
    fname = f"resumen_{key}.txt"
    if not os.path.exists(fname):
        # mensaje informativo si no existe
        text = f"{title}\n────────────────────────────────\n• No se han generado ofertas para esta categoría."
        send_message(text)
        time.sleep(1)
        continue

    with open(fname, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        content = f"{title}\n────────────────────────────────\n• No se han encontrado chollos."

    # si el archivo es demasiado grande, partir por parrafos
    if len(content) <= MAX_LEN:
        send_message(content)
    else:
        # partir por líneas en bloques que no excedan MAX_LEN
        paragraphs = content.split("\n\n")
        block = ""
        for p in paragraphs:
            if len(block) + len(p) + 2 < MAX_LEN:
                block += p + "\n\n"
            else:
                send_message(block)
                time.sleep(1)
                block = p + "\n\n"
        if block:
            send_message(block)
    time.sleep(1)  # pequeño delay entre mensajes
