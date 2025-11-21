import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

def extraer_precio(texto):
    m = re.search(r"(\d+[.,]?\d*)\s*€", texto.replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def scrape_chollo_viajes():
    url = "https://www.chollo-viajes.com/chollos-vuelos/"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    # Suponemos que las ofertas están en elementos <article> o similares
    for item in soup.select("article.offer, div.oferta, .oferta-viaje"):
        titulo = item.get_text(strip=True)
        precio = extraer_precio(titulo)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "vuelos"})
    return ofertas

def scrape_holidayguru():
    url = "https://www.holidayguru.es/ofertas-ultimo-minuto/"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".offer-item, .deal-card"):
        titulo = item.get_text(" ", strip=True)
        precio = extraer_precio(titulo)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_rumbo():
    url = "https://www.rumbo.es/es/ofertas-especiales/chollo-viaje.html"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    # Ejemplo: lo más probable es que las ofertas estén en <li> o <div> con clase especial
    for item in soup.select(".oferta, .chollo, li.offer-item"):
        titulo = item.get_text(" ", strip=True)
        precio = extraer_precio(titulo)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        if link and link.startswith("/"):
            link = "https://www.rumbo.es" + link
        ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_logitravel():
    url = "https://www.logitravel.com/viajes/chollos/"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".chollo-item, .deal-card"):
        titulo = item.get_text(" ", strip=True)
        precio = extraer_precio(titulo)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "vuelo_hotel"})
    return ofertas

def scrape_nautalia():
    url = "https://www.nautaliaviajes.com/chollos/"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("div.product, div.oferta-chollo, li.trip-item"):
        titulo = item.get_text(" ", strip=True)
        precio = extraer_precio(titulo)
        a = item.find("a", href=True)
        link = a["href"] if a else None
        ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollo_viajes())
    todas.extend(scrape_holidayguru())
    todas.extend(scrape_rumbo())
    todas.extend(scrape_logitravel())
    todas.extend(scrape_nautalia())
    # deduplicar
    seen = set()
    dedup = []
    for o in todas:
        key = (o.get("titulo"), o.get("link"))
        if key not in seen:
            seen.add(key)
            dedup.append(o)
    return dedup
