# scraper.py
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenteCazachollos/1.0)"}

def safe_get(url, timeout=12):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r.text
        print(f"[safe_get] status {r.status_code} para {url}")
    except Exception as e:
        print(f"[safe_get] error al acceder {url}: {e}")
    return None

def extraer_precio(texto):
    if not texto:
        return None
    # Buscar patrón tipo "123€" o "123 €" o "123,45€"
    m = re.search(r"(\d{1,4}(?:[.,]\d{1,2})?)\s*€", texto.replace(".", "").replace(",", "."))
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def extraer_duracion(texto):
    if not texto:
        return None
    # buscar "3 días", "4 nights", "5 noches"
    m = re.search(r"(\d{1,2})\s*(d[ií]as|days|noches|nights)", texto.lower())
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

def detectar_tipo(texto):
    t = (texto or "").lower()
    if "vuelo" in t and "hotel" in t:
        return "vuelo_hotel"
    if "hotel" in t or "noche" in t or "habitaci" in t:
        return "hoteles"
    if "vuelo" in t or "vuelos" in t or "flight" in t:
        return "vuelos"
    if "paquete" in t or "circuito" in t or "tour" in t or "pack" in t or "crucero" in t:
        return "paquetes"
    # fallback: mirar si contiene "desde X€" and "noche" -> hotel
    if "noche" in t or "noches" in t:
        return "hoteles"
    if "vuelo" in t:
        return "vuelos"
    return "paquetes"

# ---------- Scrapers (ligeros, tolerantes) ----------
def scrape_chollometro():
    url = "https://www.chollometro.com/categorias/viajes"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    # items generales
    for item in soup.select(".threadGrid .thread"):
        text = item.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = item.find("a")
        link = a["href"] if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_holidayguru():
    url = "https://www.holidayguru.es/"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for article in soup.select("article")[:80]:
        text = article.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = article.find("a")
        link = a["href"] if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_travelzoo():
    url = "https://www.travelzoo.com/es/"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for card in soup.select(".deal-card")[:60]:
        text = card.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = card.find("a")
        link = ("https://www.travelzoo.com" + a["href"]) if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_buscounchollo():
    url = "https://www.buscounchollo.com/"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for c in soup.select(".oferta")[:60]:
        text = c.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = c.find("a")
        link = a["href"] if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_destinia():
    url = "https://www.destinia.com/ofertas"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for art in soup.select("article")[:60]:
        text = art.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = art.find("a")
        link = ("https://www.destinia.com" + a["href"]) if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_atrapalo():
    url = "https://www.atrapalo.com/viajes/"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for card in soup.select(".product-card")[:60]:
        text = card.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = card.find("a")
        link = ("https://www.atrapalo.com" + a["href"]) if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_carrefour():
    url = "https://www.viajes.carrefour.es/viajes-chollos"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for art in soup.select("article")[:60]:
        text = art.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = art.find("a")
        link = a["href"] if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_logitravel():
    url = "https://www.logitravel.com/ofertas/"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for art in soup.select("article")[:60]:
        text = art.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = art.find("a")
        link = a["href"] if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_ebooking():
    url = "https://www.ebooking.com/es/ofertas/"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for art in soup.select("article")[:60]:
        text = art.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = art.find("a")
        link = a["href"] if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

def scrape_skyscanner():
    url = "https://www.skyscanner.es/inspiracion/ofertas"
    html = safe_get(url)
    if not html: return []
    soup = BeautifulSoup(html, "lxml")
    resultados = []
    for art in soup.select("article")[:60]:
        text = art.get_text(separator=" ").strip()
        price = extraer_precio(text)
        dur = extraer_duracion(text)
        a = art.find("a")
        link = ("https://www.skyscanner.es" + a["href"]) if a and a.get("href") else ""
        resultados.append({
            "titulo": text,
            "precio": price,
            "duracion": dur,
            "link": link,
            "tipo": detectar_tipo(text)
        })
    return resultados

# -------------- Combinar y normalizar --------------
def obtener_ofertas():
    fuentes = [
        scrape_chollometro,
        scrape_holidayguru,
        scrape_travelzoo,
        scrape_buscounchollo,
        scrape_destinia,
        scrape_atrapalo,
        scrape_carrefour,
        scrape_logitravel,
        scrape_ebooking,
        scrape_skyscanner
    ]

    todas = []
    for f in fuentes:
        try:
            res = f()
            if res:
                for it in res:
                    # Normalizar claves
                    titulo = it.get("titulo", "").strip()
                    precio = it.get("precio")
                    dur = it.get("duracion")
                    link = it.get("link") or ""
                    tipo = it.get("tipo") or detectar_tipo(titulo)
                    todas.append({
                        "titulo": titulo,
                        "precio": float(precio) if precio else None,
                        "duracion": int(dur) if dur else None,
                        "link": link,
                        "tipo": tipo
                    })
        except Exception as e:
            print(f"[obtener_ofertas] fallo en {f.__name__}: {e}")

    # Deduplicar por (titulo,link)
    seen = set()
    dedup = []
    for it in todas:
        key = (it["titulo"], it["link"])
        if key not in seen:
            seen.add(key)
            dedup.append(it)
    return dedup

if __name__ == "__main__":
    ops = obtener_ofertas()
    print(f"[scraper] ofertas totales: {len(ops)}")
    for o in ops[:40]:
        print(o)
