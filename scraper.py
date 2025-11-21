import requests
from bs4 import BeautifulSoup

def scrape_chollo_viajes():
    url = "https://www.chollo-viajes.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    # Buscar ofertas en la página. Esto dependerá de la estructura real
    for item in soup.select("a.chollo"):  # **Este selector es ficticio**, ajústalo según la web real
        titulo = item.get_text().strip()
        link = item.get("href")
        ofertas.append((titulo, link))
    return ofertas

def scrape_holidayguru_last_minute():
    url = "https://www.holidayguru.es/ofertas-ultimo-minuto/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    # Ejemplo de cómo podría ser: ajustar con selectores reales
    for item in soup.select(".offer-item a"):
        titulo = item.get_text().strip()
        link = item.get("href")
        ofertas.append((titulo, link))
    return ofertas

def scrape_viajes_y_chollos():
    url = "https://www.viajesychollos.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("a.oferta"):
        titulo = item.get_text().strip()
        link = item.get("href")
        ofertas.append((titulo, link))
    return ofertas

def scrape_viajes_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    ofertas = []
    for item in soup.select("a"):
        # filtrado muy básico, para ejemplo
        titulo = item.get_text().strip()
        link = item.get("href")
        if "oferta" in titulo.lower() or "chollo" in titulo.lower():
            ofertas.append((titulo, link))
    return ofertas

# Puedes añadir más funciones para otras webs, por ejemplo Liligo, Momondo, etc.

def obtener_ofertas():
    todas = []
    todas.extend(scrape_chollo_viajes())
    todas.extend(scrape_holidayguru_last_minute())
    todas.extend(scrape_viajes_y_chollos())
    todas.extend(scrape_viajes_carrefour())
    # Si añades más webs: extiende más
    return todas

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    for titulo, link in ofertas:
        print(titulo, link)
