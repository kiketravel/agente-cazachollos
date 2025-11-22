from scraper import obtener_ofertas

def rank_emoji(n):
    if n == 1: return "🥇"
    if n == 2: return "🥈"
    if n == 3: return "🥉"
    return f"{n}️⃣"

def escribir_archivo(nombre, titulo_seccion, lista):
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(titulo_seccion + "\n\n")
        if lista:
            for i, o in enumerate(lista, 1):
                linea = (
                    f"{rank_emoji(i)} {o['titulo']}\n"
                    f"Precio: {o['precio']} €\n"
                    f"Link: {o['link']}\n\n"
                )
                f.write(linea)
        else:
            f.write("No hay ofertas que cumplan los criterios.\n")


if __name__ == "__main__":
    ofertas = obtener_ofertas()

    # Asegurar ofertas con precio
    ofertas = [o for o in ofertas if o.get("precio")]

    # Normalizar texto
    for o in ofertas:
        o["titulo_lower"] = o["titulo"].lower()

    # FILTROS POR TIPO
    vuelos =     [o for o in ofertas if o["tipo"] == "vuelos" and "madrid" in o["titulo_lower"]]
    paquetes =   [o for o in ofertas if o["tipo"] == "paquetes" and "madrid" in o["titulo_lower"]]
    hoteles =    [o for o in ofertas if o["tipo"] == "hotel" and "madrid" in o["titulo_lower"]]
    vuelo_hotel =[o for o in ofertas if o["tipo"] in ("vuelo_hotel", "vuelo+hotel") and "madrid" in o["titulo_lower"]]

    # ORDENAR Y LIMITAR
    vuelos       = sorted(vuelos, key=lambda x: x["precio"])[:10]
    paquetes     = sorted(paquetes, key=lambda x: x["precio"])[:10]
    hoteles      = sorted(hoteles, key=lambda x: x["precio"])[:10]
    vuelo_hotel  = sorted(vuelo_hotel, key=lambda x: x["precio"])[:10]

    # ARCHIVOS QUE USA ENVIAR_TELEGRAM.PY
    escribir_archivo("top10_vuelos.txt",       "✈️ TOP 10 Vuelos desde Madrid", vuelos)
    escribir_archivo("top10_paquetes.txt",     "🎒 TOP 10 Paquetes desde Madrid", paquetes)
    escribir_archivo("top10_hoteles.txt",      "🏨 TOP 10 Hoteles desde Madrid", hoteles)
    escribir_archivo("top10_vuelo_hotel.txt",  "🏝️ TOP 10 Vuelo + Hotel desde Madrid", vuelo_hotel)

    print("OK: Archivos generados correctamente.")
