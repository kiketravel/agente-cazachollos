import json
import os
from scraper import obtener_ofertas

HISTORY_FILE = 'history.json'
MAX_HISTORY = 300
CATEGORIES = ["vuelos", "vuelo_hotel", "hoteles", "paquetes"]

history = {}
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)
else:
    history = {c: [] for c in CATEGORIES}

ofertas = obtener_ofertas()

cats = {c: [] for c in CATEGORIES}
for o in ofertas:
    t = o.get("tipo") or "paquetes"
    if t not in CATEGORIES:
        t = "paquetes"
    cats[t].append(o)

for c in CATEGORIES:
    combined = cats[c] + history.get(c, [])
    seen = set()
    deduped = []
    for x in combined:
        key = (x.get("titulo", ""), x.get("link", ""))
        if key not in seen:
            seen.add(key)
            deduped.append(x)
    history[c] = deduped[:MAX_HISTORY]

with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
    json.dump(history, f, ensure_ascii=False, indent=2)

# Aquí metes tu lógica de scoring / ranking para crear resumenes por categoría
