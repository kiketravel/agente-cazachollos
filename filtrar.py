# filtrar.py
import math
from scraper import obtener_ofertas
import re

# Heurísticas locales (factores por destino / palabras)
# Destinos caros -> factor < 1 (mejoran el score)
DESTINO_FACTORS = {
    "londres": 0.85,
    "paris": 0.9,
    "ny": 0.8,
    "nueva york": 0.8,
    "tokio": 0.8,
    "los angeles": 0.85,
    "madrid": 1.0,
    "barcelona": 1.0,
    "mallorca": 1.05,
    "tenerife": 1.05,
}

# Palabras que delatan "paquete" o "vuelo+hotel"
PAQUETE_KEYWORDS = ["paquete", "paquete completo", "paquetes", "todo incluido", "vuelo+hotel", "hotel+vuelo", "paquetes"]

def detect_destino(texto):
    t = (texto or "").lower()
    for k in DESTINO_FACTORS.keys():
        if k in t:
            return k
    return None

def precio_por_dia(precio, dur):
    if not precio:
        return None
    if dur and dur > 0:
        return precio / dur
    return precio

def score_heurstico(oferta):
    """
    Score: menor es mejor chollo.
    Calculado a partir de:
      - precio (obvio)
      - duración (si existe)
      - factor de destino (si detectado)
      - tipo (ajustes)
      - presencia de palabras "rebaja" o "%"
    """
    precio = oferta.get("precio")
    dur = oferta.get("duracion")
    titulo = oferta.get("titulo", "").lower()
    tipo = oferta.get("tipo", "")

    # si no hay precio, penalizamos fuertemente
    if not precio:
        return 1e9

    # base
    base = precio

    # ajustar por duración (precio por día)
    if dur and dur > 0:
        base = precio / (dur if dur > 0 else 1)

    # factor destino
    dest = detect_destino(titulo)
    dest_factor = DESTINO_FACTORS.get(dest, 1.0)

    # palabra % o rebaja: mejora el score
    discount_factor = 0.9 if re.search(r"(\b\d{1,2}%|\brebaja\b|\bdescuento\b|\boferta\b)", titulo) else 1.0

    # tipo adjustments
    type_factor = 1.0
    if tipo == "vuelos":
        type_factor = 1.0
    elif tipo == "hoteles":
        type_factor = 1.05
    elif tipo == "paquetes":
        type_factor = 0.95
    elif tipo == "vuelo_hotel":
        type_factor = 0.9

    # absurdamente bajo => boost (ej. error fare)
    boost = 1.0
    if precio and precio < 50:
        boost = 0.6

    score = base * dest_factor * discount_factor * type_factor * boost

    # proteger
    return float(score)

def agrupar_por_categoria(ofertas):
    cats = {"vuelos": [], "vuelo_hotel": [], "hoteles": [], "paquetes": []}
    for o in ofertas:
        t = o.get("tipo") or "paquetes"
        if t not in cats:
            t = "paquetes"
        cats[t].append(o)
    return cats

def ordenar_y_top(cats, top_n=10):
    resultado = {}
    for k, items in cats.items():
        # calcular score para cada item
        scored = []
        for it in items:
            s = score_heurstico(it)
            scored.append((s, it))
        # ordenar asc (mejor = menor score)
        scored.sort(key=lambda x: x[0])
        # extraer top_n
        resultado[k] = [it for s, it in scored[:top_n]]
    return resultado

def formatear_lista(items):
    """
    Formatea una lista de ofertas (ya ordenadas) en Markdown para Telegram.
    Añade medallas a los 3 primeros.
    """
    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, it in enumerate(items, start=1):
        title = it.get("titulo", "Oferta")
        link = it.get("link", "")
        precio = it.get("precio")
        dur = it.get("duracion")
        precio_text = f"{precio:.0f}€" if precio else "—"
        dur_text = f" · {dur} noches" if dur else ""
        medal = medals[i-1] + " " if i <= 3 else ""
        lines.append(f"{medal}*{i}.* {title} — *{precio_text}*{dur_text}\n👉 {link}")
    if not lines:
        return "• _No se han encontrado chollos en esta categoría._"
    return "\n\n".join(lines)

def guardar_resumen_por_categorias(topcats):
    with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
        f.write("🌟 *RESUMEN SEMANAL DE CHOLLOS* 🌟\n\n")
        order = [("vuelos","✈️ TOP 10 VUELOS"), ("vuelo_hotel","🏖️ TOP 10 VUELO+HOTEL"),
                 ("hoteles","🏨 TOP 10 HOTELES"), ("paquetes","🌍 TOP 10 PAQUETES")]
        for key, header in order:
            f.write(f"{header}\n")
            f.write("────────────────────────────────\n")
            lista = topcats.get(key, [])
            f.write(formatear_lista(lista))
            f.write("\n\n")

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    print(f"[filtrar] ofertas recogidas: {len(ofertas)}")
    cats = agrupar_por_categoria(ofertas)
    topcats = ordenar_y_top(cats, top_n=10)
    guardar_resumen_por_categorias(topcats)
    # Además guardamos un pequeño archivo por categoría para enviar cada mensaje por separado
    for k, lst in topcats.items():
        fname = f"resumen_{k}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            header_map = {
                "vuelos": "✈️ TOP 10 VUELOS",
                "vuelo_hotel": "🏖️ TOP 10 VUELO+HOTEL",
                "hoteles": "🏨 TOP 10 HOTELES",
                "paquetes": "🌍 TOP 10 PAQUETES"
            }
            f.write(f"{header_map.get(k, k)}\n────────────────────────────────\n")
            f.write(formatear_lista(lst))
    print("Archivos resumen creados por categoría.")
