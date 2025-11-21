import requests
from bs4 import BeautifulSoup
import re
import feedparser
import socket

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

# Establecer timeout global para feedparser
socket.setdefaulttimeout(30)

def extraer_precio(texto):
    m = re.search(r"(\d+[.,]?\d*)\s*€", texto.replace(",", "."))
    if m:
        try:
            return float(m.group(1))
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
            precio = extraer_precio(entry.title)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"[ERROR] No se pudo parsear RSS {url}: {e}")
    return ofertas

# Fuentes RSS reales o semi confiables
def scrape_chollometro_rss():
    url = "https://www.chollometro.com/rss"
    return parse_rss(url, tipo="paquetes")

def scrape_flightdeal_rss():
    url = "https://www.theflightdeal.com/feed"
    return parse_rss(url, tipo="vuelos")

# NOTA: no he encontrado un RSS oficial y 100% confiable para HolidayGuru con ofertas de viaje recientes
# Podrías suscribirte a su boletín, pero como RSS lo dejo comentado o como fallback.
# def scrape_holidayguru_rss():
#     url = "https://www.holidayguru.es/rss"
#     return parse_rss(url, tipo="paquetes")

# Scrapeo sencillo para Carrefour (ofertas de viaje)
def scrape_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Carrefour viajes: {e}")
        return []

    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    # selector tentativa para las ofertas
    for item in soup.select("a"):  
        text = item.get_text(" ", strip=True)
        precio = extraer_precio(text)
        link = item.get("href", "")
        if link and precio:
            if not link.startswith("http"):
                link = "https://www.viajes.carrefour.es" + link
            ofertas.append({"titulo": text, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_rumbo_chollos():
    url = "https://www.rumbo.es/es/ofertas-especiales/chollo-viaje.html"
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Rumbo: {e}")
        return []

    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("li.offer-item, .oferta, .chollo"):
        text = item.get_text(" ", strip=True)
        precio = extraer_precio(text)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        if link and precio:
            if not link.startswith("http"):
                link = "https://www.rumbo.es" + link
            ofertas.append({"titulo": text, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_logitravel():
    url = "https://www.logitravel.com/viajes/chollos/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        res.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener Logitravel: {e}")
        return []

    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".deal-card, .chollo-item"):
        text = item.get_text(" ", strip=True)
        precio = extraer_precio(text)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        if link and precio:
            if not link.startswith("http"):
                link = "https://www.logitravel.com" + link
            ofertas.append({"titulo": text, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollometro_rss())
    todas.extend(scrape_flectdeal_rss() if False else [])  # corregir nombre si se usa
    todas.extend(scrape_flightdeal_rss())
    todas.extend(scrape_carrefour())
    todas.extend(scrape_rumbo_chollos())
    todas.extend(scrape_logitravel())

    # deduplicar
    seen = set()
    dedup = []
    for o in todas:
        key = (o.get("titulo"), o.get("link"))
        if key not in seen:
            seen.add(key)
            dedup.append(o)
    return dedup

# Para test local
if __name__ == "__main__":
    ofertas = obtener_ofertas()
    print(f"Ofertas encontradas: {len(ofertas)}")
    for o in ofertas[:20]:
        print(o)
