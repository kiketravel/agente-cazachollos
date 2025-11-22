import json
from scraper import obtener_ofertas

def rank_emoji(n):
    if n == 1: return "🥇"
    if n == 2: return "🥈"
    if n == 3: return "🥉"
    return f"{n}️⃣"

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    ofertas = [o for o in ofertas if o.get("precio")]

    vuelos = [o for o in ofertas if o["tipo"] == "vuelos"]
    paquetes = [o for o in ofertas if o["tipo"] == "paquetes"]

    vuelos = sorted(vuelos, key=lambda x: x["precio"])[:10]
    paquetes = sorted(paquetes, key=lambda x: x["precio"])[:10]

    # Sin markdown, sin asteriscos, sin símbolos conflictivos
    with open("resultado_vuelos.txt", "w", encoding="utf-8") as f:
        f.write("✈️ TOP 10 Vuelos desde Madrid\n\n")
        if vuelos:
            for i, o in enumerate(vuelos, 1):
                linea = (
                    f"{rank_emoji(i)} {o['titulo']}\n"
                    f"💶 Precio: {o['precio']} €\n"
                    f"🔗 {o['link']}\n\n"
                )
                f.write(linea)
        else:
            f.write("No se han encontrado vuelos.\n")

    with open("resultado_paquetes.txt", "w", encoding="utf-8") as f:
        f.write("🏝️ TOP 10 Paquetes desde Madrid\n\n")
        if paquetes:
            for i, o in enumerate(paquetes, 1):
                linea = (
                    f"{rank_emoji(i)} {o['titulo']}\n"
                    f"💶 Precio: {o['precio']} €\n"
                    f"🔗 {o['link']}\n\n"
                )
                f.write(linea)
        else:
            f.write("No se han encontrado paquetes.\n")

    print("OK: archivos generados.")
