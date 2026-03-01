import time
import requests
import hashlib
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.tcf.gov.tr/faaliyetler/"
KEYWORD = "Pilates"

bot = Bot(token=BOT_TOKEN)

last_hash = None

def fetch_page():
    r = requests.get(URL)
    return r.text

def send_alert(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

while True:
    try:
        html = fetch_page()

        if KEYWORD in html:
            new_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()

            if last_hash is None:
                last_hash = new_hash
                send_alert("Pilates sayfada görünüyor 🎯")

            elif new_hash != last_hash:
                last_hash = new_hash
                send_alert("Sayfa güncellendi ve Pilates var 🔄")

        else:
            last_hash = None

    except Exception as e:
        send_alert(f"Hata oluştu: {e}")

    time.sleep(300)  # 5 dakika
