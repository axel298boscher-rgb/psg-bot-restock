import os
import requests
import time

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

PRODUCT_URL = "https://store.psg.fr/fr/maillot-domicile-stadium-psg-nike-25/26-flocage-champions-of-europe-26/p-357737829935687805+z-8-3250930420"

already_alerted = False

def send_alert(msg):
    requests.post(
        WEBHOOK_URL,
        json={"content": msg},
        timeout=30
    )

while True:
    try:
        r = requests.get(PRODUCT_URL, timeout=30)

        html = r.text.lower()

        stock_detected = (
            "taille s" in html
            or ">s<" in html
            or "taille m" in html
            or ">m<" in html
        )

        if stock_detected and not already_alerted:
            send_alert(
                f"🚨 POSSIBLE RESTOCK PSG !\n{PRODUCT_URL}"
            )
            already_alerted = True

        if not stock_detected:
            already_alerted = False

    except Exception as e:
        print(e)

    time.sleep(300)
