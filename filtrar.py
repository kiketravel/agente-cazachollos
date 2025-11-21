# filtrar.py
import traceback
from scraper import obtener_ofertas

PALABRAS = ["chollo", "oferta", "descuento", "rebaja", "barato", "último", "promo"]

def filtrar_chollos(ofertas):
    buenos = []
    for titulo, link in ofertas:
        t = (titulo or "").lower()
        if any(p in t for p in PALABRAS):
            buenos.append((titulo.strip(), link or ""))
    return buenos

def guardar_resumen(chollos):
    try:
        with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
            if not chollos:
                f.write("🔎 *No se han encontrado chollos relevantes esta vez.*")
                return
            f.write("🔥 *Chollos de viajes encontrados esta semana:*\n\n")
            for i, (titulo, link) in enumerate(chollos, start=1):
                # Asegurar que link sea una URL legible
                line = f"• *{titulo}*\n  👉 {link}\n\n"
                f.write(line)
    except Exception as e:
        print("Error al guardar resumen:", e)
        print(traceback.format_exc())
        # En caso de fallo al escribir el fichero, escribir un fallback mínimo
        try:
            with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
                f.write("🔎 *No se han podido generar chollos por un error interno.*")
        except:
            pass

if __name__ == "__main__":
    try:
        ofertas = obtener_ofertas()
        print(f"[filtrar] ofertas obtenidas: {len(ofertas)}")
        buenos = filtrar_chollos(ofertas)
        print(f"[filtrar] chollos filtrados: {len(buenos)}")
        guardar_resumen(buenos)
        print("resumen_chollos.txt creado.")
    except Exception as e:
        print("Error en filtrar.py:", e)
        # asegurarse de que el resumen existe aunque haya fallo
        with open("resumen_chollos.txt", "w", encoding="utf-8") as f:
            f.write("🔎 *No se han podido generar chollos por un error interno.*")
        raise
