import requests
from bs4 import BeautifulSoup
import feedparser
import json
import os

history_file = "history.json"

# Cargar historial existente
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {"vuelos": [], "hoteles": [], "paquetes": [], "vuelo_hotel": []}

def scrape_trabber():
    url = "https://www.trabber.es/rss/ofertas.xml"
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title
            link = entry.link
            precio = None
            if "€" in titulo:
                try:
                    precio = float(titulo.split("€")[0].replace(",", ".").replace("\xa0","").strip())
                except:
                    pass
            tipo = "vuelos"
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"No se pudo parsear RSS {url}: {e}")
    return ofertas

def scrape_carrefour():
    url = "https://www.carrefour.es/ofertas"
    ofertas = []
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        items = soup.select(".product-card")
        for item in items:
            titulo = item.get_text().strip()
            link = url
            precio = None
            tipo = "paquetes"
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"No se pudo obtener Carrefour: {e}")
    return ofertas

def obtener_ofertas():
    todas = []
    todas.extend(scrape_trabber())
    todas.extend(scrape_carrefour())
    # Se pueden añadir más scrapers aquí
    return todas

# Guardar en history
def actualizar_history(nuevas):
    for o in nuevas:
        tipo = o["tipo"]
        history[tipo] = [o] + history.get(tipo, [])
        if len(history[tipo]) > 300:
            history[tipo] = history[tipo][:300]

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    actualizar_history(ofertas)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"OFERTAS ENCONTRADAS: {len(ofertas)}")
    for o in ofertas:
        print(o)
