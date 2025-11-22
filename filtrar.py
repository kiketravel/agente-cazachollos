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
    # cuanto más barato respecto al histórico, mejor (0-1)
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

    # Filtrar ofertas válidas
    ofertas = [o for o in ofertas if o.get("precio")]

    for o in ofertas:
        o["titulo_lower"] = o["titulo"].lower()

    tipos = {
        "vuelos":       [o for o in ofertas if o["tipo"] == "vuelos" and "madrid" in o["titulo_lower"]],
        "hoteles":      [o for o in ofertas if o["tipo"] == "hoteles" and "madrid" in o["titulo_lower"]],
        "paquetes":     [o for o in ofertas if o["tipo"] == "paquetes" and "madrid" in o["titulo_lower"]],
        "vuelo_hotel":  [o for o in ofertas if o["tipo"] in ("vuelo_hotel","vuelo+hotel") and "madrid" in o["titulo_lower"]],
    }

    # Ordenar por scoring relativo
    for k,v in tipos.items():
        tipos[k] = sorted(v, key=lambda x: score_oferta(x, k), reverse=True)[:10]

    # Generar archivos TOP 10
    escribir_archivo("top10_vuelos.txt",      "✈️ TOP 10 Vuelos desde Madrid", tipos["vuelos"])
    escribir_archivo("top10_hoteles.txt",     "🏨 TOP 10 Hoteles desde Madrid", tipos["hoteles"])
    escribir_archivo("top10_paquetes.txt",    "🎒 TOP 10 Paquetes desde Madrid", tipos["paquetes"])
    escribir_archivo("top10_vuelo_hotel.txt", "🏝️ TOP 10 Vuelo + Hotel desde Madrid", tipos["vuelo_hotel"])

    # Guardar history actualizado
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print("OK: Archivos generados y history.json actualizado con scoring relativo.")
