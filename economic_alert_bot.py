import requests
import schedule
import time
from datetime import datetime
import pytz

# --------------------------------
# TELEGRAM SETTINGS
# --------------------------------

TELEGRAM_TOKEN = "8650266633:AAFu1eOjQdtBk-sSz-rJcrtXibLSnFCr-jo"
CHAT_ID = "7980598242"

# --------------------------------
# TELEGRAM MESSAGE FUNCTION
# --------------------------------

def send_telegram(message):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=payload)
    except:
        print("Telegram Error")


# --------------------------------
# ECONOMIC DATA
# --------------------------------

def get_economic_calendar():

    url = "https://api.tradingeconomics.com/calendar?c=guest:guest&importance=3"

    r = requests.get(url)
    data = r.json()

    today = datetime.utcnow().date()

    message = "📊 오늘의 핵심 경제지표\n\n"

    for item in data:

        country = item.get("Country")
        event = item.get("Event")
        forecast = item.get("Forecast")
        previous = item.get("Previous")
        actual = item.get("Actual")
        date = item.get("Date")

        if country in ["United States", "Japan"]:

            event_date = datetime.strptime(date[:10], "%Y-%m-%d").date()

            if event_date == today:

                message += f"""
🌎 {country}
📌 {event}

Forecast: {forecast}
Previous: {previous}
Actual: {actual}

----------------------
"""

    send_telegram(message)


# --------------------------------
# CPI / FOMC ALERT
# --------------------------------

def important_alert():

    url = "https://api.tradingeconomics.com/calendar?c=guest:guest&importance=3"

    r = requests.get(url)
    data = r.json()

    keywords = [
        "CPI",
        "PPI",
        "Interest Rate",
        "Non Farm Payroll",
        "GDP"
    ]

    for item in data:

        country = item.get("Country")
        event = item.get("Event")

        if country in ["United States", "Japan"]:

            for k in keywords:

                if k in event:

                    forecast = item.get("Forecast")
                    previous = item.get("Previous")

                    message = f"""
🚨 중요 경제지표

🌎 {country}
📌 {event}

Forecast: {forecast}
Previous: {previous}
"""

                    send_telegram(message)


# --------------------------------
# SCHEDULE
# --------------------------------

schedule.every().day.at("08:00").do(get_economic_calendar)
schedule.every().day.at("20:00").do(important_alert)


# --------------------------------
# START BOT
# --------------------------------

print("📊 Economic Telegram Bot Running...")

while True:

    schedule.run_pending()
    time.sleep(60)