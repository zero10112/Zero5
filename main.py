from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters
import openai
import os

# إعداد التوكنات
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# تحقق من التوكنات
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise Exception("Missing TELEGRAM_TOKEN or OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return 'Bot is running.'

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    dispatcher.process_update(update)
    return 'ok'

def handle_message(update, context):
    user_message = update.message.text
    chat_id = update.message.chat_id

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
        context.bot.send_message(chat_id=chat_id, text=reply)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="خطأ: " + str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)