import json
from scraper import obtener_ofertas

def rank_emoji(n):
    if n == 1: return "🥇"
    if n == 2: return "🥈"
    if n == 3: return "🥉"
    return f"{n}️⃣"

if __name__ == "__main__":
    ofertas = obtener_ofertas()

    # Solo ofertas con precio válido
    ofertas = [o for o in ofertas if o.get("precio")]

    # Filtrar por tipo
    vuelos = [o for o in ofertas if o["tipo"] == "vuelos" and "madrid" in o["titulo"].lower()]
    paquetes = [o for o in ofertas if o["tipo"] == "paquetes" and "madrid" in o["titulo"].lower()]

    # Ordenar por precio ascendente y limitar a top 10
    vuelos = sorted(vuelos, key=lambda x: x["precio"])[:10]
    paquetes = sorted(paquetes, key=lambda x: x["precio"])[:10]

    # -------------------------------
    # ARCHIVO TOP 10 VUELOS
    # -------------------------------

    with open("top10_vuelos.txt", "w", encoding="utf-8") as f:
        f.write("✈️ TOP 10 Vuelos desde Madrid\n\n")
        if vuelos:
            for i, o in enumerate(vuelos, 1):
                linea = (
                    f"{rank_emoji(i)} {o['titulo']}\n"
                    f"Precio: {o['precio']} €\n"
                    f"Link: {o['link']}\n\n"
                )
                f.write(linea)
        else:
            f.write("No hay vuelos que cumplan los criterios.\n")

    # -------------------------------
    # ARCHIVO TOP 10 PAQUETES
    # -------------------------------

    with open("top10_paquetes.txt", "w", encoding="utf-8") as f:
        f.write("🏝️ TOP 10 Paquetes desde Madrid\n\n")
        if paquetes:
            for i, o in enumerate(paquetes, 1):
                linea = (
                    f"{rank_emoji(i)} {o['titulo']}\n"
                    f"Precio: {o['precio']} €\n"
                    f"Link: {o['link']}\n\n"
                )
                f.write(linea)
        else:
            f.write("No hay paquetes que cumplan los criterios.\n")

    print("OK: top10_vuelos.txt y top10_paquetes.txt generados.")
