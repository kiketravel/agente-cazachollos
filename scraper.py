import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def safe_get(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=15)
    except:
        return None


# 1 — Chollo Viajes
def scrape_chollo_viajes():
    url = "https://www.chollo-viajes.com/"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a.chollo"):
        ofertas.append((a.get_text().strip(), a.get("href")))
    return ofertas


# 2 — HolidayGuru Último Minuto
def scrape_holidayguru():
    url = "https://www.holidayguru.es/ofertas-ultimo-minuto/"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select(".offer-item a"):
        ofertas.append((a.get_text().strip(), a.get("href")))
    return ofertas


# 3 — HolidayPirates
def scrape_holidaypirates():
    url = "https://www.holidaypirates.com/es/"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a[href*='/deals/']"):
        titulo = a.get_text().strip()
        link = a.get("href")
        if link.startswith("/"):
            link = "https://www.holidaypirates.com" + link
        ofertas.append((titulo, link))
    return ofertas


# 4 — Viajes Carrefour
def scrape_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a"):
        t = a.get_text().strip()
        if "chollo" in t.lower() or "oferta" in t.lower():
            ofertas.append((t, a.get("href")))
    return ofertas


# 5 — Liligo
def scrape_liligo():
    url = "https://www.liligo.com/es/ofertas"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    return [(a.get_text().strip(), a.get("href")) for a in soup.select("a[href*='flight']")]


# 6 — Atrapalo viajes
def scrape_atrapalo():
    url = "https://www.atrapalo.com/viajes/"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    return [(a.get_text().strip(), "https://www.atrapalo.com" + a.get("href"))
            for a in soup.select("a.card-info")]


# 7 — BuscoUnChollo
def scrape_buscounchollo():
    url = "https://www.buscounchollo.com/"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    return [(a.get_text().strip(), a.get("href")) for a in soup.select("a.oferta")]


# 8 — Lastminute
def scrape_lastminute():
    url = "https://www.lastminute.com/travel"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    return [(a.get_text().strip(), a.get("href")) for a in soup.select("a") if "deal" in a.get("href", "")]


# 9 — Logitravel
def scrape_logitravel():
    url = "https://www.logitravel.com/ofertas/"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    return [(a.get_text().strip(), a.get("href")) for a in soup.select("a") if "chollo" in a.get_text().lower()]


# 10 — Kayak Explore
def scrape_kayak():
    url = "https://www.kayak.es/explore"
    r = safe_get(url)
    if not r: return []
    return [("Kayak Explore – ver mapa", url)]


# 11 — Rumbo
def scrape_rumbo():
    url = "https://www.rumbo.es/viajes/baratos"
    r = safe_get(url)
    if not r: return []
    soup = BeautifulSoup(r.text, "lxml")
    return [(a.get_text().strip(), a.get("href")) for a in soup.select("a") if "oferta" in a.get_text().lower()]


# 12 — eDreams
def scrape_edreams():
    return [("Ofertas eDreams", "https://www.edreams.es/vuelos/ofertas/")]


# 13 — Travelzoo
def scrape_travelzoo():
    return [("Travelzoo España – ofertas", "https://www.travelzoo.com/es/")]


# 14 — Skyscanner
def scrape_skyscanner():
    return [("Skyscanner Ofertas", "https://www.skyscanner.es/ofertas")]


# 15 — Voyage Privé
def scrape_vp():
    return [("Voyage Privé", "https://www.voyage-prive.es/")]


def obtener_ofertas():
    funciones = [
        scrape_chollo_viajes,
        scrape_holidayguru,
        scrape_holidaypirates,
        scrape_carrefour,
        scrape_liligo,
        scrape_atrapalo,
        scrape_buscounchollo,
        scrape_lastminute,
        scrape_logitravel,
        scrape_kayak,
        scrape_rumbo,
        scrape_edreams,
        scrape_travelzoo,
        scrape_skyscanner,
        scrape_vp
    ]

    todas = []
    for f in funciones:
        try:
            todas.extend(f())
        except:
            pass

    return todas


if __name__ == "__main__":
    for t, l in obtener_ofertas():
        print(t, l)
