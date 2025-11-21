import os
from scraper import obtener_ofertas

def filtrar_chollos(ofertas):
    # Definir criterios para lo que consideras un chollo
    palabras_clave = ["chollo", "oferta", "descuento", "último minuto", "paquete"]
    buenos = []
    for titulo, link in ofertas:
        text = titulo.lower()
        if any(p in text for p in palabras_clave):
            buenos.append((titulo, link))
    return buenos

def guardar_resumen(chollos):
    if not chollos:
        with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
            f.write("No se han encontrado chollos relevantes esta vez.")
        return
    with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
        for titulo, link in chollos:
            f.write(f"{titulo} — {link}\n")

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    buenos = filtrar_chollos(ofertas)
    guardar_resumen(buenos)
    print(f"Encontrados {len(buenos)} chollos.")
