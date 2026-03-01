import time
import requests
import json
from bs4 import BeautifulSoup
import os

# Telegram bilgileri
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.tcf.gov.tr/faaliyetler/"
KEYWORD = "Pilates"
CHECK_INTERVAL = 300  # 5 dakika

# Daha önce görülen kursları saklamak için dosya
DATA_FILE = "seen_pilates.json"

# Önceki kursları yükle
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        seen_courses = set(json.load(f))
except:
    seen_courses = set()

def fetch_courses():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    courses = []

    # Sayfadaki faaliyetleri al
    for item in soup.find_all("div", class_="faaliyet-card"):  # class sayfaya göre değişebilir
        text = item.get_text(strip=True)
        if KEYWORD.lower() in text.lower():
            courses.append(text)
    return courses

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.get(url, params=params)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

while True:
    try:
        current_courses = fetch_courses()
        new_courses = [c for c in current_courses if c not in seen_courses]

        for course in new_courses:
            send_alert(f"Yeni Pilates kursu bulundu:\n{course}")

        if new_courses:
            seen_courses.update(new_courses)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(list(seen_courses), f, ensure_ascii=False)

    except Exception as e:
        send_alert(f"Hata oluştu: {e}")

    time.sleep(CHECK_INTERVAL)
