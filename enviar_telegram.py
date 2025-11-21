# enviar_telegram.py
import os
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Faltan TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en los secrets.")
    exit(1)

# Si no existe el resumen, enviamos un mensaje informativo en vez de fallar
if not os.path.exists("resumen_chollos.txt"):
    mensaje = "🔎 No se ha generado el resumen de chollos (archivo no encontrado)."
else:
    with open("resumen_chollos.txt", "r", encoding="utf-8") as f:
        mensaje = f.read().strip()
        if not mensaje:
            mensaje = "🔎 El resumen está vacío. No se han encontrado chollos."

# Telegram limita mensajes largos; recortar si es muy grande
MAX_LEN = 3800
if len(mensaje) > MAX_LEN:
    mensaje = mensaje[:MAX_LEN-200] + "\n\n...(mensaje recortado)...\nVisita las fuentes para más info."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}

try:
    r = requests.post(url, data=data, timeout=15)
    if r.status_code == 200:
        print("Mensaje enviado correctamente a Telegram.")
    else:
        print("Error al enviar a Telegram:", r.status_code, r.text)
        # intentar enviar un mensaje de error pequeño
        try:
            err_msg = "⚠️ Error al enviar chollos: " + str(r.status_code)
            requests.post(url, data={"chat_id": CHAT_ID, "text": err_msg})
        except:
            pass
except Exception as e:
    print("Excepción al enviar mensaje a Telegram:", e)
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": "⚠️ Excepción al intentar enviar chollos."})
    except:
        pass
    exit(1)
