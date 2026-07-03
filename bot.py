from flask import Flask, request
import telebot
import datetime
import requests

TOKEN = "8954781131:AAFJ1UVU2YXtLdr_5ooItHv4o4kQUNvI_M0"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def translate_to_english(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fa&tl=en&dt=t&q={text}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0][0][0]
    except:
        pass
    return "❌ ترجمه انجام نشد!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 سلام! ربات روی سرور روشن شد!")

@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(message, f"🕐 {now}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text.startswith('/'):
        translated = translate_to_english(message.text)
        bot.reply_to(message, f"🔹 {translated}")

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def home():
    return "ربات روشن است!", 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR_APP_NAME.onrender.com/' + TOKEN)
    app.run()
