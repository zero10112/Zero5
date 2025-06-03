import logging
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import os

# توكن البوت
TELEGRAM_TOKEN = "7989535235:AAGr1JVXAQ6_h9QretU-SwVuhQuA1tY3lho"
# مفتاح OpenAI
openai.api_key = "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"

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("حصل خطأ أثناء المعالجة.")
        logging.error(f"Error from OpenAI: {e}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())