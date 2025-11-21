import os

def filtrar_chollos(ofertas):
    palabras_clave = ["vuelo", "hotel", "viaje"]
    buenos = []
    for titulo, link in ofertas:
        if any(p in titulo.lower() for p in palabras_clave):
            buenos.append((titulo, link))
    return buenos

if __name__ == "__main__":
    import scraper
    ofertas = scraper.obtener_ofertas()
    buenos = filtrar_chollos(ofertas)
    for t, l in buenos:
        print("CHOLLO:", t, l)
