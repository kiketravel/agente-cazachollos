import requests
from bs4 import BeautifulSoup
import re

# -----------------------------------------------------------
# HELPERS
# -----------------------------------------------------------

def extraer_precio(texto):
    """Extrae el primer precio encontrado en un string."""
    match = re.search(r"(\d+)[\.,]?\d*\s?€", texto)
    return float(match.group(1)) if match else None


def limpiar(texto):
    return re.sub(r"\s+", " ", texto).strip()


# -----------------------------------------------------------
# SCRAPERS POR SITIO
# -----------------------------------------------------------

def scrape_chollometro():
    url = "https://www.chollometro.com/categorias/viajes"
    try:
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html, "html.parser")

        resultados = []
        cards = soup.select(".threadGrid")[:50]  # muchos results

        for c in cards:
            title = limpiar(c.select_one(".thread-title").get_text())
            price_text = c.select_one(".thread-price")
            price = extraer_precio(price_text.get_text()) if price_text else None
            link = c.select_one("a")["href"]

            resultados.append({
                "titulo": title,
                "precio": price,
                "link": link,
                "tipo": detectar_tipo(title)
            })

        return resultados

    except Exception as e:
        print("Error en Chollometro", e)
        return []


def scrape_holidayguru():
    url = "https://www.holidayguru.es/"
    try:
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html, "html.parser")

        resultados = []
        items = soup.select("article")[:50]

        for it in items:
            title = limpiar(it.get_text())
            price = extraer_precio(title)
            link_tag = it.find("a")
            link = link_tag["href"] if link_tag else None

            if price and link:
                resultados.append({
                    "titulo": title,
                    "precio": price,
                    "link": link,
                    "tipo": detectar_tipo(title)
                })

        return resultados

    except Exception:
        return []


def scrape_travelzoo():
    url = "https://www.travelzoo.com/es/"
    try:
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html, "html.parser")

        resultados = []
        items = soup.select(".deal-card")[:40]

        for it in items:
            title = limpiar(it.get_text())
            price = extraer_precio(title)
            link_tag = it.find("a")
            link = "https://www.travelzoo.com" + link_tag["href"] if link_tag else None

            resultados.append({
                "titulo": title,
                "precio": price,
                "link": link,
                "tipo": detectar_tipo(title)
            })

        return resultados

    except Exception:
        return []


def scrape_buscounchollo():
    url = "https://www.buscounchollo.com/"
    try:
        html = requests.get(url, timeout=20).text
        s
