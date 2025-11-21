import json
import os
from scraper import obtener_ofertas

HISTORY_FILE = 'history.json'
MAX_HISTORY = 300
CATEGORIES = ["vuelos", "paquetes"]

history = {}
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = json.load(f)
else:
    history = {c: [] for c in CATEGORIES}

ofertas = obtener_ofertas()

cats = {c: [] for c in CATEGORIES}
for o in ofertas:
    t = o.get("tipo", "paquetes")
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

# Generar resumen simple
for c in CATEGORIES:
    fname = f"resumen_{c}.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"**{c.upper()}**\n\n")
        for o in cats[c][:10]:
            titulo = o.get("titulo", "–")
            link = o.get("link", "")
            precio = o.get("precio")
            precio_txt = f"{precio:.0f}€" if precio else "–"
            f.write(f"- {titulo} — {precio_txt}\n  {link}\n")
