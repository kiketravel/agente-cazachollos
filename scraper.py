import requests
from bs4 import BeautifulSoup
import feedparser
import json
import os
import re
import sys

sys.stdout.reconfigure(line_buffering=True)

history_file = "history.json"
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {"vuelos": [], "hoteles": [], "paquetes": [], "vuelo_hotel": []}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def actualizar_history(ofertas):
    for o in ofertas:
        tipo = o["tipo"]
        if tipo not in history:
            history[tipo] = []
        history[tipo].append(o)
        history[tipo] = history[tipo][-300:]
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print("[INFO] history.json actualizado", flush=True)

def scrape_logitravel_vuelos():
    print("[INFO] Scrapeando Logitravel vuelos...", flush=True)
    url = "https://www.logitravel.com/vuelos/chollos/"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        cards = soup.select(".clearfix .offer-item, .deal-card")
        for card in cards:
            texto = card.get_text(" ", strip=True)
            precio = None
            m = re.search(r"(\d+[.,]?\d*)\s*€", texto)
            if m:
                precio = float(m.group(1).replace(",", "."))
            link_tag = card.find("a", href=True)
            link = link_tag["href"] if link_tag else None
            if link and precio:
                ofertas.append({"titulo": texto, "link": link, "precio": precio, "tipo": "vuelos"})
    except Exception as e:
        print("[ERROR] Logitravel vuelos:", e, flush=True)
    print(f"[INFO] Logitravel vuelos: {len(ofertas)} ofertas extraídas.", flush=True)
    return ofertas

def scrape_viajesychollos():
    print("[INFO] Scrapeando ViajesYChollos...", flush=True)
    url = "https://www.viajesychollos.com/"
    ofertas = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        # Suponiendo que las ofertas están en <a> con clase chollo
        for a in soup.select("a"):
            texto = a.get_text(" ", strip=True)
            precio = None
            m = re.search(r"(\d+[.,]?\d*)\s*€", texto)
            if m:
                precio = float(m.group(1).replace(",", "."))
            link = a.get("href")
            if link and precio:
                ofertas.append({"titulo": texto, "link": link, "precio": precio, "tipo": "paquetes"})
    except Exception as e:
        print("[ERROR] ViajesYChollos:", e, flush=True)
    print(f"[INFO] ViajesYChollos: {len(ofertas)} ofertas extraídas.", flush=True)
    return ofertas

def scrape_rss(url, tipo):
    print(f"[INFO] Scrapeando RSS {tipo} desde {url}", flush=True)
    ofertas = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.get("title", "")
            link = entry.get("link", "")
            precio = None
            m = re.search(r"(\d+[.,]?\d*)\s*€", titulo)
            if m:
                precio = float(m.group(1).replace(",", "."))
            ofertas.append({"titulo": titulo, "link": link, "precio": precio, "tipo": tipo})
    except Exception as e:
        print(f"[ERROR] RSS {url} fallo:", e, flush=True)
    print(f"[INFO] RSS {tipo}: {len(ofertas)} ofertas extraídas.", flush=True)
    return ofertas

def obtener_ofertas():
    print("[INFO] Iniciando obtención de ofertas...", flush=True)
    todas = []
    todas.extend(scrape_logitravel_vuelos())
    todas.extend(scrape_viajesychollos())

    rss_list = [
        ("https://www.theflightdeal.com/feed", "vuelos"),
        ("https://www.holidaypirates.com/rss", "paquetes"),
        ("https://www.viajes.com/rss/chollos.xml", "paquetes"),
    ]
    for url, tipo in rss_list:
        todas.extend(scrape_rss(url, tipo))

    validas = [o for o in todas if o.get("precio") is not None]
    print(f"[INFO] Total ofertas válidas: {len(validas)}", flush=True)
    return validas

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    actualizar_history(ofertas)
    print("[INFO] Ofertas extraídas:", flush=True)
    for o in ofertas[:10]:
        print(o, flush=True)
    print("[INFO] Scraper finalizado.", flush=True)
