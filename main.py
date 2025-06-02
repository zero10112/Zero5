import os
import logging
import openai
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=200
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error from OpenAI: {e}")
        reply = "حصل خطأ، حاول مرة ثانية."

    await update.message.reply_text(reply)

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route('/')
def home():
    return "Bot is running"

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return 'ok'

if __name__ == '__main__':
    application.run_polling()