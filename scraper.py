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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_trabber():
    """Scraper RSS Trabber"""
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
            if precio and "Madrid" in titulo:
                ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"[ERROR] No se pudo parsear RSS Trabber: {e}")
    return ofertas

def scrape_travelzoo():
    """Scraper RSS TravelZoo España"""
    url = "https://www.travelzoo.com/es/rss"
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title
            link = entry.link
            precio = None
            # Buscar precio en título
            import re
            m = re.search(r"(\d+[.,]?\d*) ?€", titulo)
            if m:
                precio = float(m.group(1).replace(",", "."))
            tipo = "paquetes"
            if precio:
                ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"[ERROR] No se pudo parsear RSS TravelZoo: {e}")
    return ofertas

def scrape_carrefour():
    """Scraper HTML Carrefour ofertas viajes"""
    url = "https://www.carrefour.es/ofertas"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        items = soup.select("div.productCard")  # ajustar según HTML real
        for it in items:
            titulo = it.select_one("a.productCard-title")
            precio_tag = it.select_one("span.price")
            if titulo and precio_tag:
                t = titulo.get_text(strip=True)
                p_text = precio_tag.get_text(strip=True).replace("€","").replace(",",".")
                try:
                    precio = float(p_text)
                except:
                    precio = None
                if precio:
                    ofertas.append({"titulo": t, "link": it.a["href"], "precio": precio, "tipo": "paquetes"})
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Carrefour: {e}")
    return ofertas

def ofertas_prueba():
    """Ofertas de prueba si no se encuentra nada real"""
    return [
        {"titulo":"Vuelo Madrid - Oslo 5 días","link":"https://example.com/vuelo1","precio":120.0,"tipo":"vuelos"},
        {"titulo":"Hotel Madrid Centro 3 noches","link":"https://example.com/hotel1","precio":80.0,"tipo":"hoteles"},
        {"titulo":"Paquete Madrid + Paris 4 días","link":"https://example.com/paquete1","precio":200.0,"tipo":"paquetes"},
    ]

def obtener_ofertas():
    todas = []
    todas.extend(scrape_trabber())
    todas.extend(scrape_travelzoo())
    todas.extend(scrape_carrefour())

    print(f"[DEBUG] Ofertas encontradas antes de filtro Madrid: {len(todas)}")
    
    # Filtrar solo ofertas con precio y origen Madrid si es aplicable
    filtradas = []
    for o in todas:
        if o.get("precio"):
            if o["tipo"] == "vuelos" and "Madrid" not in o["titulo"]:
                continue
            filtradas.append(o)
    
    if not filtradas:
        print("[INFO] No se encontraron ofertas reales, usando ofertas de prueba")
        filtradas = ofertas_prueba()
    
    print(f"[DEBUG] Ofertas válidas: {len(filtradas)}")
    for o in filtradas:
        print(o)
    return filtradas

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
