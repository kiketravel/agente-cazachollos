# scraper.py
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

def safe_get(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r
        print(f"[safe_get] status {r.status_code} para {url}")
        return None
    except Exception as e:
        print(f"[safe_get] error al acceder {url}: {e}")
        return None

# 1 — Chollo Viajes
def scrape_chollo_viajes():
    url = "https://www.chollo-viajes.com/"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a.chollo"):
        titulo = a.get_text().strip()
        link = a.get("href")
        ofertas.append((titulo, link))
    return ofertas

# 2 — HolidayGuru
def scrape_holidayguru():
    url = "https://www.holidayguru.es/ofertas-ultimo-minuto/"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select(".offer-item a"):
        titulo = a.get_text().strip()
        link = a.get("href")
        ofertas.append((titulo, link))
    return ofertas

# 3 — HolidayPirates
def scrape_holidaypirates():
    url = "https://www.holidaypirates.com/es/"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a[href*='/deals/']"):
        titulo = a.get_text().strip()
        link = a.get("href")
        if link and link.startswith("/"):
            link = "https://www.holidaypirates.com" + link
        ofertas.append((titulo, link))
    return ofertas

# 4 — Viajes Carrefour
def scrape_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a"):
        t = a.get_text().strip()
        link = a.get("href")
        if link and ("chollo" in t.lower() or "oferta" in t.lower()):
            ofertas.append((t, link))
    return ofertas

# 5 — Liligo
def scrape_liligo():
    url = "https://www.liligo.com/es/ofertas"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a[href*='flight']"):
        titulo = a.get_text().strip()
        link = a.get("href")
        ofertas.append((titulo, link))
    return ofertas

# 6 — Atrapalo
def scrape_atrapalo():
    url = "https://www.atrapalo.com/viajes/"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a.card-info"):
        titulo = a.get_text().strip()
        href = a.get("href")
        link = href if href.startswith("http") else "https://www.atrapalo.com" + href
        ofertas.append((titulo, link))
    return ofertas

# 7 — BuscoUnChollo
def scrape_buscounchollo():
    url = "https://www.buscounchollo.com/"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a.oferta"):
        titulo = a.get_text().strip()
        link = a.get("href")
        ofertas.append((titulo, link))
    return ofertas

# 8 — Lastminute (simple)
def scrape_lastminute():
    url = "https://www.lastminute.com/travel"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a"):
        href = a.get("href", "")
        if "deal" in href or "offers" in href:
            titulo = a.get_text().strip()
            ofertas.append((titulo, href))
    return ofertas

# 9 — Logitravel
def scrape_logitravel():
    url = "https://www.logitravel.com/ofertas/"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a"):
        t = a.get_text().strip()
        if "chollo" in t.lower() or "oferta" in t.lower():
            ofertas.append((t, a.get("href")))
    return ofertas

# 10 — Kayak Explore (link directo)
def scrape_kayak():
    url = "https://www.kayak.es/explore"
    return [("Kayak Explore – ver mapa", url)]

# 11 — Rumbo
def scrape_rumbo():
    url = "https://www.rumbo.es/viajes/baratos"
    r = safe_get(url)
    if not r:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    ofertas = []
    for a in soup.select("a"):
        t = a.get_text().strip()
        if "oferta" in t.lower() or "chollo" in t.lower():
            ofertas.append((t, a.get("href")))
    return ofertas

# 12 — eDreams (link directo)
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
            resultado = f()
            if resultado:
                # normalizar enlaces relativos
                for titulo, link in resultado:
                    if link and link.startswith("/"):
                        # no sabemos dominio, dejar tal cual o prefixar si es necesario
                        todas.append((titulo, link))
                    else:
                        todas.append((titulo, link))
        except Exception as e:
            print(f"[obtener_ofertas] fallo en {f.__name__}: {e}")
    # deduplicar por (titulo,link)
    seen = set()
    dedup = []
    for t, l in todas:
        key = (t.strip(), (l or "").strip())
        if key not in seen:
            seen.add(key)
            dedup.append((t.strip(), l or ""))
    return dedup

if __name__ == "__main__":
    ops = obtener_ofertas()
    print(f"[scraper] ofertas totales: {len(ops)}")
    for t, l in ops[:50]:
        print(t, l)
