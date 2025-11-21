import requests
import os

# -------------------------------
# CONFIGURACIÓN
# -------------------------------

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# -------------------------------
# LECTURA DEL ARCHIVO
# -------------------------------

with open("resumen_chollos.txt", "r", encoding="utf-8") as f:
    contenido = f.read()

# -------------------------------
# FORMATO MÁS AMIGABLE
# -------------------------------

mensaje = f"""
🌟 *RESUMEN SEMANAL DE CHOLLOS* 🌟

Aquí tienes tu selección TOP 10 de vuelos, hoteles y paquetes más bestias de la semana.

────────────────────────────────

{contenido}

────────────────────────────────
💬 *Fin del reporte semanal*
"""

# -------------------------------
# ENVÍO A TELEGRAM
# -------------------------------

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

resp = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": mensaje,
    "parse_mode": "Markdown"
})

print("Enviado a Telegram:", resp.text)
