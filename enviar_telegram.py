import os
import requests
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BASE = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

for cat in ["vuelos", "paquetes"]:
    fname = f"resumen_{cat}.txt"
    if not os.path.exists(fname):
        msg = f"No se han generado ofertas para **{cat}**."
    else:
        with open(fname, "r", encoding="utf-8") as f:
            msg = f.read()

    # dividir si es muy largo
    partes = msg.split("\n\n")
    texto = ""
    for p in partes:
        if len(texto) + len(p) + 4 < 3800:
            texto += p + "\n\n"
        else:
            requests.post(BASE, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
            time.sleep(1)
            texto = p + "\n\n"
    if texto:
        requests.post(BASE, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
        time.sleep(1)
