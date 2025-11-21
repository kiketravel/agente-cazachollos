import json
import os
from scraper import obtener_ofertas

HISTORY_FILE = 'history.json'
MAX_HISTORY = 300
CATEGORIES = ["vuelos", "paquetes", "vuelo_hotel", "hoteles"]

# Cargar histórico
history = {}
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)
else:
    history = {c: [] for c in CATEGORIES}

# Obtener ofertas actuales
ofertas = obtener_ofertas()

# Organizar por categoría
cats = {c: [] for c in CATEGORIES}
for o in ofertas:
    t = o.get("tipo", "paquetes")
    if t not in CATEGORIES:
        t = "paquetes"
    cats[t].append(o)

# Actualizar histórico
for c in CATEGORIES:
    combined = cats[c] + history.get(c, [])
    seen = set()
    deduped = []
    for x in combined:
        key = (x.get("titulo",""), x.get("link",""))
        if key not in seen:
            seen.add(key)
            deduped.append(x)
    history[c] = deduped[:MAX_HISTORY]

with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
    json.dump(history, f, ensure_ascii=False, indent=2)

# Generar resumen TOP 10 por categoría
for c in CATEGORIES:
    fname = f"resumen_{c}.txt"
    ofertas_cat = cats[c]
    # Ordenar por precio ascendente
    ofertas_cat = [o for o in ofertas_cat if o.get("precio") is not None]
    ofertas_cat.sort(key=lambda x: x.get("precio"))
    top10 = ofertas_cat[:10]

    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"✈️ *TOP {len(top10)} {c.upper()}* ✈️\n\n")
        for idx, o in enumerate(top10, start=1):
            titulo = o.get("titulo","–")
            link = o.get("link","")
            precio = o.get("precio")
            precio_txt = f"{precio:.0f}€" if precio else "–"
            # Emoji según ranking
            if idx == 1:
                rank_emoji = "🥇"
            elif idx == 2:
                rank_emoji = "🥈"
            elif idx == 3:
                rank_emoji = "🥉"
            else:
                rank_emoji = "⭐"  # <-- CORREGIDO
            f.write(f"{
