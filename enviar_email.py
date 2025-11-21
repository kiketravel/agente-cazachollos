import os
import smtplib
from email.mime.text import MIMEText
import filtrar
import scraper

# Obtener ofertas filtradas
ofertas = scraper.obtener_ofertas()
buenos = filtrar.filtrar_chollos(ofertas)
contenido = "\n".join([f"{t}: {l}" for t, l in buenos])

# Configuración de correo
user = os.environ['EMAIL_USER']
password = os.environ['EMAIL_PASS']
to = os.environ['EMAIL_TO']

msg = MIMEText(contenido)
msg['Subject'] = 'Resumen Semanal de Chollos'
msg['From'] = user
msg['To'] = to

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(user, password)
    server.send_message(msg)
