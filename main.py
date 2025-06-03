import os
import openai
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters, Application

# إعدادات المفاتيح
TELEGRAM_TOKEN = "7989535235:AAGr1JVXAQ6_h9QretU-SwVuhQuA1tY3lho"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

async def handle_message(update: Update, context):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "❌ خطأ في الاتصال بـ ChatGPT."

    await bot.send_message(chat_id=chat_id, text=reply)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app.dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return "بوت ChatGPT شغال ✅"

def main():
    app.dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)
    app.dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    main()