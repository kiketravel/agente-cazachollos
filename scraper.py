import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

def extraer_precio(texto):
    m = re.search(r'\d+[,.]?\d*', texto.replace(',', '.'))
    return float(m.group().replace(',', '.')) if m else 0.0

def scrape_chollometro():
    url = "https://www.chollometro.com/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".threadGrid"):
        titulo_tag = item.select_one(".thread-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".thread-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = "https://www.chollometro.com" + link_tag["href"]
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_holidayguru():
    url = "https://www.holidayguru.es/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".deal-card"):
        titulo_tag = item.select_one(".deal-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".deal-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.holidayguru.es" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_travelzoo():
    url = "https://www.travelzoo.com/es/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".deal"):
        titulo_tag = item.select_one(".deal-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".deal-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.travelzoo.com" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_buscounchollo():
    url = "https://www.buscounchollo.com/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".oferta-item"):
        titulo_tag = item.select_one(".titulo")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".precio")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.buscounchollo.com" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_destinia():
    url = "https://www.destinia.com/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".product-card"):
        titulo_tag = item.select_one(".product-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".product-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.destinia.com" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "vuelo_hotel"})
    return ofertas

def scrape_atrapalo():
    url = "https://www.atrapalo.com/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".product-item"):
        titulo_tag = item.select_one(".product-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".product-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.atrapalo.com" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "paquetes"})
    return ofertas

def scrape_carrefour():
    url = "https://www.carrefour.es/ofertas"
    res = requests.get(url, headers=HEADERS)
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

def scrape_logitravel():
    url = "https://www.logitravel.com/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".deal-card"):
        titulo_tag = item.select_one(".deal-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".deal-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.logitravel.com" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "vuelo_hotel"})
    return ofertas

def scrape_ebooking():
    url = "https://www.ebooking.com/"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".deal-item"):
        titulo_tag = item.select_one(".title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.ebooking.com" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "hoteles"})
    return ofertas

def scrape_skyscanner():
    url = "https://www.skyscanner.net/deals"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".deal-card"):
        titulo_tag = item.select_one(".deal-title")
        link_tag = item.select_one("a")
        precio_tag = item.select_one(".deal-price")
        if titulo_tag and link_tag and precio_tag:
            titulo = titulo_tag.text.strip()
            link = link_tag.get("href", "")
            if not link.startswith("http"):
                link = "https://www.skyscanner.net" + link
            precio = extraer_precio(precio_tag.text)
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": "vuelos"})
    return ofertas

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollometro())
    todas.extend(scrape_holidayguru())
    todas.extend(scrape_travelzoo())
    todas.extend(scrape_buscounchollo())
    todas.extend(scrape_destinia())
    todas.extend(scrape_atrapalo())
    todas.extend(scrape_carrefour())
    todas.extend(scrape_logitravel())
    todas.extend(scrape_ebooking())
    todas.extend(scrape_skyscanner())
    return todas
