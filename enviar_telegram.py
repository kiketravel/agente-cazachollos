import os
import requests
import json

def enviar_telegram(mensaje):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("ERROR: TELEGRAM_TOKEN o TELEGRAM_CHAT_ID no están disponibles.")
        print("TOKEN:", token)
        print("CHAT:", chat_id)
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        print("Enviado correctamente.")
    except Exception as e:
        print("ERROR enviando Telegram:", e)


# ---------------------------
# ENVÍO DE LOS 4 FICHEROS
# ---------------------------

ficheros = [
    ("✈️ <b>TOP 10 Vuelos</b>\n\n", "top10_vuelos.txt"),
    ("🏨 <b>TOP 10 Hoteles</b>\n\n", "top10_hoteles.txt"),
    ("🌍 <b>TOP 10 Paquetes</b>\n\n", "top10_paquetes.txt"),
    ("🧳 <b>TOP 10 Vuelo + Hotel</b>\n\n", "top10_vuelo_hotel.txt")
]

for cabecera, fichero in ficheros:
    if os.path.exists(fichero):
        with open(fichero, "r", encoding="utf-8") as f:
            contenido = f.read().strip()

        if contenido:
            enviar_telegram(cabecera + contenido)
        else:
            enviar_telegram(cabecera + "No hay ofertas esta semana.")
    else:
        enviar_telegram(cabecera + "No existe el fichero generado.")
