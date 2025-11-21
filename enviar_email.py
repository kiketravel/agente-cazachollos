import os
import smtplib
from email.mime.text import MIMEText

# Cargar secrets
user = os.environ['SMTP_USER']
password = os.environ['SMTP_PASS']
host = os.environ['SMTP_HOST']
port = int(os.environ['SMTP_PORT'])
to = os.environ['EMAIL_TO']

# Leer el resumen de chollos
with open("resumen_chollos.txt", "r", encoding="utf-8") as f:
    mensaje = f.read()

msg = MIMEText(mensaje, "html", "utf-8")  # Puedes enviar HTML
msg['Subject'] = "Resumen semanal de chollos"
msg['From'] = user
msg['To'] = to

# Enviar correo
with smtplib.SMTP(host, port) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

print("Correo enviado correctamente.")
