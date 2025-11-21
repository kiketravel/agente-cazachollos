import requests
from bs4 import BeautifulSoup
import re
import feedparser

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

def extraer_precio(texto):
    m = re.search(r"(\d+[.,]?\d*)\s*€", texto.replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

# ------------------- RSS Parsers -------------------

def parse_rss(url, tipo="paquetes"):
    ofertas = []
    feed = feedparser.parse(url)
    for entry in feed.entries:
        titulo = entry.title
        link = entry.link
        precio = extraer_precio(entry.title)
        ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    return ofertas

def scrape_chollometro_rss():
    url = "https://www.chollometro.com/rss"
    return parse_rss(url, tipo="paquetes")

def scrape_holidayguru_rss():
    url = "https://www.holidayguru.es/rss"
    return parse_rss(url, tipo="paquetes")

def scrape_travelzoo_rss():
    url = "https://www.travelzoo.com/es/rss"
    return parse_rss(url, tipo="paquetes")

def scrape_rumbo_rss():
    url = "https://www.rumbo.es/rss/chollos.xml"
    return parse_rss(url, tipo="vuelo_hotel")

# ------------------- Carrefour Scraper -------------------

def scrape_carrefour():
    url = "https://www.carrefour.es/ofertas"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".product-card"):
        titulo_tag = item.select_one(".product-name")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.carrefour.es" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

# ------------------- Obtener todas las ofertas -------------------

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollometro_rss())
    todas.extend(scrape_holidayguru_rss())
    todas.extend(scrape_travelzoo_rss())
    todas.extend(scrape_rumbo_rss())
    todas.extend(scrape_carrefour())
    # deduplicar
    seen = set()
    dedup = []
    for o in todas:
        key = (o.get("titulo"), o.get("link"))
        if key not in seen:
            seen.add(key)
            dedup.append(o)
    return dedup
