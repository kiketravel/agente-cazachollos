import json
from scraper import obtener_ofertas, history, actualizar_history, history_file

def rank_emoji(n):
    if n == 1: return "🥇"
    if n == 2: return "🥈"
    if n == 3: return "🥉"
    return f"{n}️⃣"

def score_oferta(oferta, tipo):
    precios = [o['precio'] for o in history.get(tipo, []) if o.get('precio')]
    if not precios:
        return 0
    precio_min = min(precios)
    precio_max = max(precios)
    score = (precio_max - oferta['precio']) / (precio_max - precio_min + 1e-6)
    return score

def escribir_archivo(nombre, titulo_seccion, lista):
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(titulo_seccion + "\n\n")
        if lista:
            for i, o in enumerate(lista, 1):
                linea = (
                    f"{rank_emoji(i)} {o['titulo']}\n"
                    f"💶 Precio: {o['precio']} €\n"
                    f"🔗 {o['link']}\n\n"
                )
                f.write(linea)
        else:
            f.write("No hay ofertas que cumplan los criterios.\n")

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    actualizar_history(ofertas)

    # Filtrar ofertas válidas y origen Madrid si aplica
    ofertas = [o for o in ofertas if o.get("precio") and (o["tipo"]!="vuelos" or "Madrid" in o["titulo"])]

    tipos = {
        "vuelos": [o for o in ofertas if o["tipo"] == "vuelos"],
        "hoteles": [o for o in ofertas if o["tipo"] == "hoteles"],
        "paquetes": [o for o in ofertas if o["tipo"] == "paquetes"],
        "vuelo_hotel": [o for o in ofertas if o["tipo"] in ("vuelo_hotel","vuelo+hotel")],
    }

    # Ordenar por scoring relativo y TOP 10
    for k,v in tipos.items():
        tipos[k] = sorted(v, key=lambda x: score_oferta(x, k), reverse=True)[:10]

    # Generar archivos siempre
    escribir_archivo("top10_vuelos.txt",      "✈️ TOP 10 Vuelos desde Madrid", tipos["vuelos"])
    escribir_archivo("top10_hoteles.txt",     "🏨 TOP 10 Hoteles desde Madrid", tipos["hoteles"])
    escribir_archivo("top10_paquetes.txt",    "🎒 TOP 10 Paquetes desde Madrid", tipos["paquetes"])
    escribir_archivo("top10_vuelo_hotel.txt", "🏝️ TOP 10 Vuelo + Hotel desde Madrid", tipos["vuelo_hotel"])

    # Guardar history actualizado
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print("OK: Archivos generados y history.json actualizado con scoring relativo.")
