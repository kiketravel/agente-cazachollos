import os
import requests
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BASE = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

CATEGORIES = ["vuelos", "paquetes", "vuelo_hotel", "hoteles"]

for cat in CATEGORIES:
    fname = f"resumen_{cat}.txt"
    if not os.path.exists(fname):
        msg = f"No se han generado ofertas para **{cat}**."
        requests.post(BASE, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        continue

    with open(fname, "r", encoding="utf-8") as f:
        contenido = f.read()

    # Telegram limita a 4096 caracteres, dividimos si es necesario
    mensajes = []
    while contenido:
        if len(contenido) <= 3800:
            mensajes.append(contenido)
            break
        else:
            # Cortamos por líneas
            corte = contenido[:3800].rfind("\n")
            mensajes.append(contenido[:corte])
            contenido = contenido[corte:].lstrip("\n")

    for m in mensajes:
        requests.post(BASE, json={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"})
        time.sleep(1)
