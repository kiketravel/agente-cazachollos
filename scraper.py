import requests
from bs4 import BeautifulSoup
import re
import feedparser
import socket

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

socket.setdefaulttimeout(30)

def extraer_precio(texto):
    texto = texto.replace(",", ".")
    # Buscar precio en euros
    m = re.search(r"(\d{1,4}(?:\.\d{1,2})?)\s*€", texto)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    # si no hay €, ver si hay un número y asumirlo (menos seguro)
    m2 = re.search(r"(\d{1,4}(?:\.\d{1,2})?)", texto)
    if m2:
        try:
            return float(m2.group(1))
        except:
            return None
    return None

def parse_rss(url, tipo="paquetes", filtrar_madrid=False):
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.get("title", "")
            descripcion = entry.get("description", "")
            link = entry.get("link", "")
            combinado = (titulo + " " + descripcion).strip()
            if filtrar_madrid and "Madrid" not in combinado:
                continue
            precio = extraer_precio(combinado)
            ofertas.append({
                "titulo": titulo.strip(),
                "link": link,
                "precio": precio,
                "tipo": tipo
            })
    except Exception as e:
        print(f"[ERROR] parse_rss para {url}: {e}")
    return ofertas

def scrape_the_flight_deal():
    url = "https://www.theflightdeal.com/feed"
    # No filtro Madrid aquí, porque la mayoría de ofertas de vuelos no mencionan ciudad de origen
    return parse_rss(url, tipo="vuelos", filtrar_madrid=False)

def scrape_fly4free():
    url = "https://www.fly4free.com/feed/"
    return parse_rss(url, tipo="vuelos", filtrar_madrid=False)

def scrape_holidaypirates():
    url = "https://www.holidaypirates.com/rss"  # este es un ejemplo (no garantizo que funcione siempre)
    return parse_rss(url, tipo="paquetes", filtrar_madrid=False)

def scrape_trabber_madrid():
    url = "https://www.trabber.es/feeds/offers?from_city=MAD&daily_offers=2&type=rss_2.0"
    return parse_rss(url, tipo="vuelos", filtrar_madrid=True)

def scrape_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] al obtener Carrefour viajes: {e}")
        return ofertas

    soup = BeautifulSoup(res.text, "lxml")
    for a in soup.select("a"):
        texto = a.get_text(" ", strip=True)
        link = a.get("href", "")
        precio = extraer_precio(texto)
        if not link or precio is None:
            continue
        if "Madrid" not in texto and "madrid" not in link.lower():
            continue
        if not link.startswith("http"):
            link = "https://www.viajes.carrefour.es" + link
        ofertas.append({
            "titulo": texto,
            "link": link,
            "precio": precio,
            "tipo": "paquetes"
        })
    return ofertas

def obtener_ofertas():
    todas = []
    todas.extend(scrape_the_flight_deal())
    todas.extend(scrape_fly4free())
    todas.extend(scrape_holidaypirates())
    todas.extend(scrape_trabber_madrid())
    todas.extend(scrape_carrefour())

    # Deduplicar
    seen = set()
    dedup = []
    for o in todas:
        key = (o.get("titulo"), o.get("link"))
        if key not in seen:
            seen.add(key)
            dedup.append(o)
    return dedup

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    print("Ofertas encontradas:", len(ofertas))
    for o in ofertas:
        print(o)
