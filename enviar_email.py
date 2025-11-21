import os
import smtplib
from email.mime.text import MIMEText

# Verificar existencia del resumen
if not os.path.exists("resumen_chollos.txt"):
    print("No se encontró resumen_chollos.txt. No se enviará email.")
    exit(0)

with open("resumen_chollos.txt", "r", encoding="utf-8") as f:
    mensaje = f.read()

user = os.environ['SMTP_USER']
password = os.environ['SMTP_PASS']
host = os.environ['SMTP_HOST']
port = int(os.environ['SMTP_PORT'])
to = os.environ['EMAIL_TO']

msg = MIMEText(mensaje, "plain", "utf-8")
msg['Subject'] = "Resumen semanal de chollos de viajes"
msg['From'] = user
msg['To'] = to

with smtplib.SMTP(host, port) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

print("Correo enviado correctamente.")
