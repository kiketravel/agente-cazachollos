import os
import requests

def enviar_mensaje_telegram(chat_id, token, mensaje):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": mensaje, "parse_mode": "HTML"}
    try:
        res = requests.post(url, data=data, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] enviando Telegram: {e}")

def leer_archivo(nombre):
    try:
        with open(nombre, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return f"No se pudo leer {nombre}"

if __name__ == "__main__":
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] No se han encontrado los secrets de Telegram")
        exit(1)

    archivos = [
        ("top10_vuelos.txt", "✈️ Vuelos"),
        ("top10_hoteles.txt", "🏨 Hoteles"),
        ("top10_paquetes.txt", "🎒 Paquetes"),
        ("top10_vuelo_hotel.txt", "🏝️ Vuelo + Hotel"),
    ]

    for fichero, titulo in archivos:
        contenido = leer_archivo(fichero)
        mensaje = f"📣 {titulo}\n\n{contenido}"
        enviar_mensaje_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mensaje)
        print(f"[INFO] Enviado mensaje {titulo}")
