import requests
from bs4 import BeautifulSoup
import re
import feedparser
import socket

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

# Timeout global para feedparser y requests
socket.setdefaulttimeout(30)

def extraer_precio(texto):
    """Extrae precio en Euros de un texto, devolviendo float"""
    texto = texto.replace(",", ".").replace("€", "").replace("EUR", "").strip()
    m = re.findall(r"\d+\.?\d*", texto)
    if m:
        try:
            return float(m[0])
        except:
            return None
    return None

def parse_rss(url, tipo="paquetes"):
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title
            link = entry.link
            if "Madrid" not in titulo:
                continue
            precio = extraer_precio(entry.title)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"[ERROR] No se pudo parsear RSS {url}: {e}")
    return ofertas

# ---------- Fuentes ----------

def scrape_chollometro_rss():
    url = "https://www.chollometro.com/rss"
    return parse_rss(url, tipo="paquetes")

def scrape_flightdeal_rss():
    url = "https://www.theflightdeal.com/feed"
    return parse_rss(url, tipo="vuelos")

def scrape_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Carrefour viajes: {e}")
        return []

    soup = BeautifulSoup(res.text, "lxml")
    for item in soup.select("a"):
        text = item.get_text(" ", strip=True)
        link = item.get("href", "")
        if not link.startswith("http"):
            link = "https://www.viajes.carrefour.es" + link
        precio = extraer_precio(text)
        if precio and "Madrid" in text:
            ofertas.append({"titulo": text, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_rumbo_chollos():
    url = "https://www.rumbo.es/es/ofertas-especiales/chollo-viaje.html"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Rumbo: {e}")
        return []

    soup = BeautifulSoup(res.text, "lxml")
    for item in soup.select("li.offer-item, .oferta, .chollo"):
        text = item.get_text(" ", strip=True)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        if link and not link.startswith("http"):
            link = "https://www.rumbo.es" + link
        precio = extraer_precio(text)
        if precio and "Madrid" in text:
            ofertas.append({"titulo": text, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_logitravel():
    url = "https://www.logitravel.com/viajes/chollos/"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Logitravel: {e}")
        return []

    soup = BeautifulSoup(res.text, "lxml")
    for item in soup.select(".deal-card, .chollo-item"):
        text = item.get_text(" ", strip=True)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        if link and not link.startswith("http"):
            link = "https://www.logitravel.com" + link
        precio = extraer_precio(text)
        if precio and "Madrid" in text:
            ofertas.append({"titulo": text, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

# ---------- Obtener todas las ofertas ----------

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollometro_rss())
    todas.extend(scrape_flightdeal_rss())
    todas.extend(scrape_carrefour())
    todas.extend(scrape_rumbo_chollos())
    todas.extend(scrape_logitravel())

    # Deduplicar
    seen = set()
    dedup = []
    for o in todas:
        key = (o.get("titulo"), o.get("link"))
        if key not in seen:
            seen.add(key)
            dedup.append(o)
    return dedup

# ---------- Test local ----------

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    print(f"Se han encontrado {len(ofertas)} ofertas desde Madrid.")
    for o in ofertas[:20]:
        print(o)
