import requests
from bs4 import BeautifulSoup
import feedparser
import json
import os

# Archivo de history
history_file = "history.json"
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {"vuelos":[], "hoteles":[], "paquetes":[], "vuelo_hotel":[]}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def actualizar_history(ofertas):
    for o in ofertas:
        tipo = o["tipo"]
        if tipo not in history:
            history[tipo] = []
        history[tipo].append(o)
        # Mantener solo últimos 300
        history[tipo] = history[tipo][-300:]

# ---------------------------
# Scrapers de ejemplo
# ---------------------------

def scrape_carrefour():
    url = "https://www.carrefour.es/ofertas"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        items = soup.select("div.productCard")  # ajustar según HTML real
        for it in items:
            try:
                titulo_tag = it.select_one("a.productCard-title")
                precio_tag = it.select_one("span.price")
                if not titulo_tag or not precio_tag:
                    continue
                t = titulo_tag.get_text(strip=True)
                p_text = precio_tag.get_text(strip=True).replace("€","").replace(",",".")
                precio = float(p_text)
                ofertas.append({"titulo": t, "link": it.a["href"], "precio": precio, "tipo": "paquetes"})
            except Exception as e:
                print(f"[WARN] Error parseando un item de Carrefour: {e}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo obtener Carrefour: {e}")
    return ofertas

def scrape_trabber():
    """Scraper de ejemplo para vuelos, devuelve siempre datos de prueba"""
    ofertas = []
    try:
        url = "https://www.trabber.es/ofertas-vuelos"
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        # Ejemplo simplificado: siempre devolver 2 vuelos
        ofertas.append({
            "titulo": "119,00 € Madrid - Oslo (5 días)",
            "link": "https://www.trabber.es/offer-detail?orig=mad&dest=osl",
            "precio": 119.0,
            "tipo": "vuelos"
        })
        ofertas.append({
            "titulo": "122,25 € Madrid - Berlín (4 días)",
            "link": "https://www.trabber.es/offer-detail?orig=mad&dest=ber",
            "precio": 122.25,
            "tipo": "vuelos"
        })
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo obtener Trabber: {e}")
    return ofertas

def scrape_rss(url, tipo):
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            try:
                titulo = entry.title
                link = entry.link
                precio = None
                # Extraer precio si aparece en title
                import re
                m = re.search(r"(\d+[.,]?\d*)\s?€", titulo)
                if m:
                    precio = float(m.group(1).replace(",","."))
                ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
            except Exception as e:
                print(f"[WARN] Error parseando RSS item {url}: {e}")
    except Exception as e:
        print(f"[ERROR] No se pudo parsear RSS {url}: {e}")
    return ofertas

def obtener_ofertas():
    todas = []

    # Ejemplos de fuentes
    todas.extend(scrape_carrefour())
    todas.extend(scrape_trabber())
    
    # RSS de prueba
    rss_list = [
        ("https://www.viajes.com/rss/chollos.xml", "paquetes"),
        ("https://www.travelzoo.com/es/rss", "vuelos"),
        ("https://www.hotelscombined.com/rss/chollos.xml", "hoteles"),
        ("https://www.tripadvisor.com/rss", "hoteles"),
        ("https://www.kayak.com/rss", "vuelo_hotel"),
    ]
    for url, tipo in rss_list:
        todas.extend(scrape_rss(url, tipo))
    
    # Solo ofertas con precio
    todas = [o for o in todas if o.get("precio")]
    
    print(f"OFERTAS ENCONTRADAS: {len(todas)}")
    return todas

# Prueba rápida
if __name__ == "__main__":
    ofertas = obtener_ofertas()
    actualizar_history(ofertas)
    print("History actualizado, ofertas ejemplo:")
    for o in ofertas[:5]:
        print(o)
