import requests
from bs4 import BeautifulSoup

def obtener_ofertas():
    url = "https://www.chollometro.com/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    ofertas = []
    for item in soup.select(".thread-title a"):
        titulo = item.text.strip()
        link = "https://www.chollometro.com" + item['href']
        ofertas.append((titulo, link))
    
    return ofertas

if __name__ == "__main__":
    ofertas = obtener_ofertas()
    for t, l in ofertas:
        print(t, l)
