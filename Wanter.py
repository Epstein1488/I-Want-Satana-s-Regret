import os, time, requests
from bs4 import BeautifulSoup

NICK = os.environ["NICK"]
TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]
URL = f"https://www.rucoyonline.com/characters/{NICK.replace(' ', '%20')}"
OLD = ("hour", "day", "week", "month", "year")

def last_online():
    html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20).text
    for row in BeautifulSoup(html, "html.parser").find_all("tr"):
        c = row.find_all(["td", "th"])
        if len(c) >= 2 and "last online" in c[0].get_text().lower():
            return c[1].get_text(strip=True)

for _ in range(5):
    try:
        cur = last_online()
        if cur and not any(w in cur.lower() for w in OLD):
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT, "text": f"🟢 {NICK} в сети! ({cur})"},
                timeout=15,
            )
            break
    except Exception as e:
        print(e)
    time.sleep(60)
