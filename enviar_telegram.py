import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def enviar(mensaje):
    if not mensaje.strip():
        return

    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"  # seguro incluso con emojis y links
    }

    try:
        r = requests.post(URL, json=payload, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print("ERROR enviando Telegram:", e)

def enviar_archivo(nombre):
    if not os.path.exists(nombre):
        print(f"NO existe {nombre}")
        return

    with open(nombre, "r", encoding="utf-8") as f:
        contenido = f.read().strip()

    if contenido:
        enviar(contenido)
    else:
        print(f"{nombre} está vacío")

if __name__ == "__main__":
    enviar_archivo("resultado_vuelos.txt")
    enviar_archivo("resultado_paquetes.txt")
