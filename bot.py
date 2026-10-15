import json
import os
import urllib.parse
import urllib.request

import feedparser

# ====== A MODIFIER ======
MOTS_CLES = ["bon plan sneakers", "promo Nike", "soldes baskets", "Maison Margiela promo"]
LANGUE, PAYS = "fr", "FR"
MAX_PAR_SUJET = 5
# ========================

FICHIER_VUS = "deja_vus.json"
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def charger_vus():
    try:
        with open(FICHIER_VUS, encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def sauver_vus(vus):
    with open(FICHIER_VUS, "w", encoding="utf-8") as f:
        json.dump(sorted(vus)[-2000:], f)


def envoyer(texte):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": texte,
        "disable_web_page_preview": "true",
    }).encode()
    urllib.request.urlopen(url, data, timeout=20)


def main():
    vus = charger_vus()
    for mot in MOTS_CLES:
        q = urllib.parse.quote(mot)
        flux = feedparser.parse(
            f"https://news.google.com/rss/search?q={q}"
            f"&hl={LANGUE}&gl={PAYS}&ceid={PAYS}:{LANGUE}"
        )
        nouveaux = [a for a in flux.entries if a.link not in vus]
        for art in nouveaux[:MAX_PAR_SUJET]:
            envoyer(f"📰 [{mot}]\n{art.title}\n{art.link}")
        vus.update(a.link for a in nouveaux)
    sauver_vus(vus)


if __name__ == "__main__":
    main()
