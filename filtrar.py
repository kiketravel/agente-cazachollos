import json
from scraper import obtener_ofertas

def rank_emoji(n):
    if n == 1: return "🥇"
    if n == 2: return "🥈"
    if n == 3: return "🥉"
    return f"{n}️⃣"

if __name__ == "__main__":
    print("[INFO] Ejecutando filtrar.py...", flush=True)
    ofertas = obtener_ofertas()
    ofertas = [o for o in ofertas if o.get("precio")]

    tipos = ["vuelos", "hoteles", "paquetes", "vuelo_hotel"]
    for tipo in tipos:
        lista = [o for o in ofertas if o["tipo"] == tipo]
        lista = sorted(lista, key=lambda x: x["precio"])[:10]
        filename = f"resultado_{tipo}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"🔹 TOP 10 {tipo.capitalize()} desde Madrid\n\n")
            if lista:
                for i, o in enumerate(lista, 1):
                    f.write(f"{rank_emoji(i)} {o['titulo']}\n")
                    f.write(f"💶 Precio: {o['precio']} €\n")
                    f.write(f"🔗 {o['link']}\n\n")
            else:
                f.write(f"No se han encontrado {tipo}.\n")
        print(f"[INFO] Archivo generado: {filename}", flush=True)
    print("[INFO] filtrar.py finalizado.", flush=True)
