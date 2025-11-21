from scraper import obtener_ofertas

PALABRAS = ["chollo", "oferta", "descuento", "rebaja", "barato", "último", "promo"]

def filtrar_chollos(ofertas):
    buenos = []
    for titulo, link in ofertas:
        t = titulo.lower()
        if any(p in t for p in PALABRAS):
            buenos.append((titulo.strip(), link))
    return buenos

def guardar_resumen(chollos):
    with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
        if not chollos:
            f.write("🔎 *No se han encontrado chollos esta vez.*")
            return

        f.write("🔥 *Chollos de viajes encontrados esta semana:*\n\n")
        for titulo, link in chollos:
            f.write(f"• *{titulo}*\n  👉 {link}\n\n")
