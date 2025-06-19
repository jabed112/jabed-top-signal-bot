import os
import requests
import time
import telegram
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

def fetch_data():
    url = "https://api.ignice.com/game-history"
    response = requests.get(url)
    data = response.json()
    return data

def analyze_and_signal(data):
    try:
        last_round = data[-1]
        num = int(last_round['number'])
        total = sum(int(x) for x in str(num))
        diff = abs(int(str(num)[0]) - int(str(num)[-1]))
        if total % 2 == 0 and diff < 5:
            return "✅ Signal: BIG"
        else:
            return "✅ Signal: SMALL"
    except:
        return "❌ Error analyzing data."

def main():
    while True:
        try:
            data = fetch_data()
            signal = analyze_and_signal(data)
            bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            bot.send_message(chat_id=CHAT_ID, text=f"Error: {str(e)}")
        time.sleep(60)

if __name__ == "__main__":
    main()
