import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import openai

TOKEN = "8160586658:AAGGFpDdsIUar2sYKrt0ZgdOP3rRpfLMRfM"
OPENAI_API_KEY = "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"

app = Flask(__name__)
bot = Bot(token=TOKEN)
openai.api_key = OPENAI_API_KEY

@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    message = update.message.text

    # إرسال النص إلى OpenAI والرد
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )

    reply = response['choices'][0]['message']['content']
    await bot.send_message(chat_id=update.message.chat.id, text=reply)

    return 'ok'

@app.route('/')
def index():
    return "بوت شغال ✅"

if __name__ == '__main__':
    from telegram.ext import Application

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, webhook))

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))