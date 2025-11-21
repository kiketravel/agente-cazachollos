import requests
from bs4 import BeautifulSoup
import re
import feedparser
import socket

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

# Poner timeout global para conexiones
socket.setdefaulttimeout(30)

def extraer_precio(texto):
    """
    Extrae el primer precio de tipo EUR en el texto.
    Si hay otros precios (USD), se ignoran.
    """
    # Reemplazar coma por punto, limpiar símbolo euro
    texto = texto.replace(",", ".")
    # Buscar patrones tipo "1234.56 €" o "1234€"
    m = re.search(r"(\d{1,4}(?:\.\d{1,2})?)\s*€", texto)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    # Si no hay “€” explícito, buscar número y asumir euro (riesgoso)
    m2 = re.search(r"(\d{1,4}(?:\.\d{1,2})?)", texto)
    if m2:
        try:
            return float(m2.group(1))
        except:
            return None
    return None

def parse_rss(url, tipo="paquetes"):
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title or ""
            descripcion = entry.get("description", "")
            link = entry.link
            combined = titulo + " " + descripcion
            # Filtrar Madrid
            if "Madrid" not in combined:
                continue
            precio = extraer_precio(combined)
            ofertas.append({
                "titulo": titulo.strip(),
                "link": link,
                "precio": precio,
                "tipo": tipo
            })
    except Exception as e:
        print(f"[ERROR] parse_rss para {url}: {e}")
    return ofertas

# RSS fiables para ofertas de viaje
def scrape_chollometro_rss():
    return parse_rss("https://www.chollometro.com/rss", tipo="paquetes")

def scrape_flightdeal_rss():
    return parse_rss("https://www.theflightdeal.com/feed", tipo="vuelos")

def scrape_travelzoo_rss():
    return parse_rss("https://www.travelzoo.com/es/rss", tipo="paquetes")

def scrape_holidaypirates_rss():
    return parse_rss("https://www.holidaypirates.com/rss", tipo="paquetes")

def scrape_lastminute_rss():
    return parse_rss("https://www.lastminute.com/rss", tipo="paquetes")

# Scraping para Carrefour viajes
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
    # Buscar elementos <a> con ofertas
    for a in soup.select("a"):
        texto = a.get_text(" ", strip=True)
        link = a.get("href", "")
        precio = extraer_precio(texto)
        if not link or not precio:
            continue
        # Filtrar Madrid
        if "Madrid" not in texto:
            # también mirar si "MAD" aparece o parte de URL
            if "madrid" not in link.lower():
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
    todas.extend(scrape_chollometro_rss())
    todas.extend(scrape_flightdeal_rss())
    todas.extend(scrape_travelzoo_rss())
    todas.extend(scrape_holidaypirates_rss())
    todas.extend(scrape_lastminute_rss())
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
    print(f"Ofertas encontradas: {len(ofertas)}")
    for o in ofertas:
        print(o)
