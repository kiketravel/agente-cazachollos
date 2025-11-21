import os
import requests

# Verificar existencia del resumen
if not os.path.exists("resumen_chollos.txt"):
    print("No se encontró resumen_chollos.txt. No se enviará mensaje.")
    exit(0)

with open("resumen_chollos.txt", "r", encoding="utf-8") as f:
    mensaje = f.read()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not all([TOKEN, CHAT_ID]):
    print("Faltan variables de Telegram. Revisa tus GitHub Secrets.")
    exit(1)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": mensaje,
    "parse_mode": "Markdown"  # opcional
}

try:
    r = requests.post(url, data=data)
    if r.status_code == 200:
        print("Mensaje enviado correctamente a Telegram.")
    else:
        print(f"Error al enviar mensaje: {r.status_code}, {r.text}")
except Exception as e:
    print(f"Excepción al enviar mensaje: {e}")
    exit(1)
