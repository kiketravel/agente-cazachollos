import requests
from bs4 import BeautifulSoup

def scrape_chollo_viajes():
    url = "https://www.chollo-viajes.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("a.chollo"):  # Ajustar según la web real
        titulo = item.get_text().strip()
        link = item.get("href")
        ofertas.append((titulo, link))
    return ofertas

def scrape_holidayguru_last_minute():
    url = "https://www.holidayguru.es/ofertas-ultimo-minuto/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select(".offer-item a"):
        titulo = item.get_text().strip()
        link = item.get("href")
        ofertas.append((titulo, link))
    return ofertas

def scrape_holidaypirates_es():
    url = "https://www.holidaypirates.com/es/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("a[href*='/deals/']"):  # Selector básico para ofertas
        titulo = item.get_text().strip()
        link = item.get("href")
        if link.startswith("/"):
            link = "https://www.holidaypirates.com" + link
        ofertas.append((titulo, link))
    return ofertas

def scrape_viajes_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("a"):
        titulo = item.get_text().strip()
        link = item.get("href")
        if "oferta" in titulo.lower() or "chollo" in titulo.lower():
            ofertas.append((titulo, link))
    return ofertas

def scrape_liligo():
    url = "https://www.liligo.com/es/ofertas"
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        ofertas = []
        for item in soup.select("a[href*='flights']"):
            titulo = item.get_text().strip()
            link = item.get("href")
            ofertas.append((titulo, link))
        return ofertas
    except Exception:
        return []  # En caso de fallo, retornar lista vacía

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollo_viajes())
    todas.extend(scrape_holidayguru_last_minute())
    todas.extend(scrape_holidaypirates_es())
    todas.extend(scrape_viajes_carrefour())
    todas.extend(scrape_liligo())
    return todas

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    for titulo, link in ofertas:
        print(titulo, link)
