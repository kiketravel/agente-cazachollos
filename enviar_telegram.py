import os
import requests

def enviar_mensaje(texto, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": texto, "parse_mode":"Markdown"})
        r.raise_for_status()
        print(f"[INFO] Mensaje enviado correctamente ({len(texto)} caracteres)", flush=True)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] enviando Telegram: {e}", flush=True)

if __name__ == "__main__":
    print("[INFO] Ejecutando enviar_telegram.py...", flush=True)
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[ERROR] No se han encontrado los secrets TELEGRAM_TOKEN/TELEGRAM_CHAT_ID", flush=True)
        exit(1)

    archivos = ["resultado_vuelos.txt", "resultado_hoteles.txt", "resultado_paquetes.txt", "resultado_vuelo_hotel.txt"]
    for file in archivos:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                texto = f.read()
                enviar_mensaje(texto, token, chat_id)
        else:
            print(f"[WARN] No existe fichero generado: {file}", flush=True)
    print("[INFO] enviar_telegram.py finalizado.", flush=True)
