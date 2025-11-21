# filtrar.py
import traceback
from scraper import obtener_ofertas

PALABRAS = ["chollo", "oferta", "descuento", "rebaja", "barato", "último", "promo"]

# Reglas simples para clasificar
def clasificar(titulo):
    t = titulo.lower()

    # Vuelos
    if "vuelo" in t or "vuelos" in t or "flight" in t:
        return "vuelos"

    # Hoteles
    if "hotel" in t and "vuelo" not in t:
        return "hoteles"

    # Paquetes
    if "paquete" in t or "circuito" in t or "tour" in t or "crucero" in t:
        return "paquetes"

    # Vuelo + Hotel
    if "vuelo" in t and "hotel" in t:
        return "vuelo_hotel"

    # fallback
    if "hotel" in t:
        return "hoteles"
    if "vuelo" in t:
        return "vuelos"
    return "paquetes"


def es_chollo(titulo):
    t = titulo.lower()
    return any(p in t for p in PALABRAS)


def filtrar_y_clasificar(ofertas):
    cats = {
        "vuelos": [],
        "paquetes": [],
        "vuelo_hotel": [],
        "hoteles": []
    }

    for titulo, link in ofertas:
        if not titulo:
            continue
        if not es_chollo(titulo):
            continue

        categoria = clasificar(titulo)
        cats[categoria].append((titulo.strip(), link))

    return cats


def top10_por_categoria(categorias):
    resultado = {}
    for cat, items in categorias.items():
        # Limitar a 10
        resultado[cat] = items[:10]
    return resultado


def guardar_resumen(cats):
    with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
        f.write("🔥 **TOP CHOLLOS DE VIAJES – Resumen Semanal**\n\n")

        secciones = [
            ("vuelos", "✈️ *TOP 10 Vuelos baratos*"),
            ("vuelo_hotel", "🌍 *TOP 10 Vuelo + Hotel*"),
            ("hoteles", "🏨 *TOP 10 Hoteles*"),
            ("paquetes", "🧳 *TOP 10 Paquetes*")
        ]

        for key, titulo in secciones:
            f.write(f"{titulo}\n")
            ofertas = cats.get(key, [])
            if not ofertas:
                f.write("• No se han encontrado chollos esta semana.\n\n")
                continue

            for idx, (t, link) in enumerate(ofertas, start=1):
                f.write(f"{idx}. *{t}*\n   👉 {link}\n")

            f.write("\n")


if __name__ == "__main__":
    try:
        ofertas = obtener_ofertas()
        print(f"[filtrar] ofertas obtenidas: {len(ofertas)}")

        categorias = filtrar_y_clasificar(ofertas)
        topcats = top10_por_categoria(categorias)

        guardar_resumen(topcats)

        print("resumen_chollos.txt creado con TOP 10 por categoría.")

    except Exception as e:
        print("Error en filtrar.py:", e)
        print(traceback.format_exc())

        with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
            f.write("⚠️ Error interno generando el resumen semanal.")
