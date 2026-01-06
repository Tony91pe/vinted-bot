import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode
import time

# Variabili d'ambiente
BOT_TOKEN = os.getenv("8520348977:AAGPOF9A7JqGltmDVj9zMnlhGW1OlY4i5FY")
CHAT_ID = os.getenv("6696383223")
VINTED_URL = os.getenv("VINTED_URL")

# Parole chiave da monitorare
KEYWORDS = ["iphone", "ipad", "macbook", "apple", "airpods"]

# Inizializza il bot
bot = Bot(token=BOT_TOKEN)

# Archivio per evitare doppie notifiche
seen_links = set()

def estrai_annunci():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(VINTED_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("div.feed-grid__item")

risultati = []
for item in items:
    link_tag = item.select_one("a")
if not link_tag:
        continue

     url = "https://www.vinted.it" + link_tag["href"]
if url in seen_links:
        continue

    titolo = item.select_one("h2")
    prezzo = item.select_one("div[class*=price]")
    immagine_tag = item.select_one("img")
    
    testo = (titolo.text if titolo else "").lower()
    if not any(keyword in testo for keyword in KEYWORDS):
        continue
    
    immagine = immagine_tag["src"] if immagine_tag else None
    prezzo_text = prezzo.text.strip() if prezzo else "Prezzo non disponibile"
    
    risultati.append({
    "titolo": titolo.text.strip() if titolo else "Senza titolo",
    "prezzo": prezzo_text,
    "url": url,
    "immagine": immagine
    })
    seen_links.add(url)
    return risultati

def invia_notifica(annuncio):
    messaggio = f"📱 <b>{annuncio['titolo']}</b>\n💶 <b>{annuncio['prezzo']}</b>\n🔗 <a href=\"{annuncio['url']}\">Apri annuncio</a>\n\n🔧 <i>Segnalazione automatica Dolomiti Tech Lab</i>"
    if annuncio["immagine"]:
        bot.send_photo(chat_id=CHAT_ID, photo=annuncio["immagine"], caption=messaggio, parse_mode=ParseMode.HTML)
    else:
        bot.send_message(chat_id=CHAT_ID, text=messaggio, parse_mode=ParseMode.HTML)

def main():
    while True:
        try:
            annunci = estrai_annunci()
            for annuncio in annunci:
                invia_notifica(annuncio)
        except Exception as e:
           print("Errore:", e)
        time.sleep(60)

if __name__ == "__main__":
    main()
