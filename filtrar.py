import json
from scraper import obtener_ofertas

def rank_emoji(n):
    if n == 1:
        return "🥇"
    if n == 2:
        return "🥈"
    if n == 3:
        return "🥉"
    return f"#{n}"

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    ofertas = [o for o in ofertas if o.get("precio")]

    vuelos = [o for o in ofertas if o["tipo"] == "vuelos"]
    paquetes = [o for o in ofertas if o["tipo"] == "paquetes"]

    vuelos = sorted(vuelos, key=lambda x: x["precio"])[:10]
    paquetes = sorted(paquetes, key=lambda x: x["precio"])[:10]

    with open("resultado_vuelos.txt", "w") as f:
        f.write("✈️ *TOP 10 Vuelos desde Madrid*\n\n")
        for i, o in enumerate(vuelos, 1):
            f.write(f"{rank_emoji(i)} {o['titulo']} — {o['precio']} €\n{o['link']}\n\n")

    with open("resultado_paquetes.txt", "w") as f:
        f.write("🏝️ *TOP 10 Paquetes desde Madrid*\n\n")
        for i, o in enumerate(paquetes, 1):
            f.write(f"{rank_emoji(i)} {o['titulo']} — {o['precio']} €\n{o['link']}\n\n")

    print("OK: archivos generados.")
