import requests
from bs4 import BeautifulSoup
import feedparser
import re
import socket

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.1)"}
socket.setdefaulttimeout(25)

def contiene_madrid(texto):
    texto = texto.lower()
    claves = ["madrid", "mad", "desde madrid", "from madrid", "from mad", "origin mad"]
    return any(c in texto for c in claves)

def extraer_precio(texto):
    texto = texto.replace(",", ".")
    m = re.search(r"(\d{2,4}(?:\.\d{1,2})?)\s*€", texto)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def parse_rss(url, tipo="paquetes", exige_madrid=True):
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.get("title", "")
            desc = entry.get("description", "")
            link = entry.get("link", "")

            full = (titulo + " " + desc).strip()
            if exige_madrid and not contiene_madrid(full):
                continue

            precio = extraer_precio(full)
            if precio is None:
                continue

            ofertas.append({
                "titulo": titulo.strip(),
                "link": link,
                "precio": precio,
                "tipo": tipo
            })

    except Exception as e:
        print("RSS ERROR", url, e)

    return ofertas

# -------- FUENTES -------- #

def scrape_fly4free():
    return parse_rss(
        "https://www.fly4free.com/feed/",
        tipo="vuelos",
        exige_madrid=True
    )

def scrape_theflightdeal():
    return parse_rss(
        "https://www.theflightdeal.com/feed/",
        tipo="vuelos",
        exige_madrid=True
    )

def scrape_trabber():
    # Este feed está específicamente filtrado ya para MAD
    return parse_rss(
        "https://www.trabber.es/feeds/offers?from_city=MAD&daily_offers=2&type=rss_2.0",
        tipo="vuelos",
        exige_madrid=False  # ya viene filtrado en el feed
    )

def scrape_holidaypirates():
    return parse_rss(
        "https://www.holidaypirates.com/rss",
        tipo="paquetes",
        exige_madrid=True
    )

def scrape_carrefour():
    ofertas = []
    url = "https://www.viajes.carrefour.es/viajes-chollos"

    try:
        res = requests.get(url, headers=HEADERS, timeout=25)
        res.raise_for_status()
    except Exception:
        return ofertas

    soup = BeautifulSoup(res.text, "lxml")

    for card in soup.select("a"):
        texto = card.get_text(" ", strip=True)
        link = card.get("href", "")

        if not contiene_madrid(texto):
            continue

        precio = extraer_precio(texto)
        if precio is None:
            continue

        if link and not link.startswith("http"):
            link = "https://www.viajes.carrefour.es" + link

        ofertas.append({
            "titulo": texto,
            "link": link,
            "precio": precio,
            "tipo": "paquetes"
        })

    return ofertas

# -------- MASTER -------- #

def obtener_ofertas():
    todas = []
    todas += scrape_fly4free()
    todas += scrape_theflightdeal()
    todas += scrape_trabber()
    todas += scrape_holidaypirates()
    todas += scrape_carrefour()

    # dedupe
    seen = set()
    final = []
    for o in todas:
        key = (o["titulo"], o["link"])
        if key not in seen:
            seen.add(key)
            final.append(o)

    return final

if __name__ == "__main__":
    o = obtener_ofertas()
    print("OFERTAS ENCONTRADAS:", len(o))
    for x in o:
        print(x)
