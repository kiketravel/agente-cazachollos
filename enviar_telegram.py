import os
import requests
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
CATEGORIES = ["vuelos", "vuelo_hotel", "hoteles", "paquetes"]
MAX_LEN = 3800

for key in CATEGORIES:
    fname = f'resumen_{key}.txt'
    if not os.path.exists(fname):
        send_text = f'No hay ofertas para {key}'
        requests.post(BASE_URL, json={"chat_id": CHAT_ID, "text": send_text, "parse_mode":"Markdown"})
        continue

    with open(fname,'r',encoding='utf-8') as f:
        content = f.read()

    blocks = []
    lines = content.split('\n\n')
    block = ''
    for l in lines:
        if len(block) + len(l) + 2 < MAX_LEN:
            block += l + '\n\n'
        else:
            blocks.append(block)
            block = l + '\n\n'
    if block:
        blocks.append(block)

    for b in blocks:
        requests.post(BASE_URL, json={"chat_id": CHAT_ID, "text": b, "parse_mode":"Markdown"})
        time.sleep(1)
