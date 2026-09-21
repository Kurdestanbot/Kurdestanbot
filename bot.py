import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

try:
    with open("data.txt", "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except FileNotFoundError:
    KNOWLEDGE_BASE = "داده‌ای یافت نشد."

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="سلام! من راهنمای گردشگری کردستان هستم. چطور می‌تونم کمکتون کنم؟"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    prompt = f"""شما یک راهنمای گردشگری متخصص برای استان کردستان هستید. 
فقط و فقط بر اساس اطلاعات زیر به سوالات پاسخ دهید. 
اگر پاسخ در اطلاعات زیر نبود، صادقانه بگویید که اطلاعاتی در این مورد ندارید.

اطلاعات مرجع:
{KNOWLEDGE_BASE}

سوال کاربر: {user_message}
"""
    try:
        response = client.chat.completions.create(
            model="google/gemini-flash-1.5",
            messages=[
                {"role": "system", "content": "You are a helpful tourism assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        bot_reply = response.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)
    except Exception as e:
        logging.error(f"Error: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="مشکلی پیش آمد. بعداً تلاش کنید.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    PORT = int(os.environ.get("PORT", 10000))
    URL = os.environ.get("RENDER_EXTERNAL_URL")
    
    if URL:
        # این بخش وب‌سرور رو باز می‌کنه تا Render راضی بشه
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=os.environ.get("TELEGRAM_TOKEN"),
            webhook_url=f"{URL}/{os.environ.get('TELEGRAM_TOKEN')}"
        )
    else:
        application.run_polling()import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

try:
    with open("data.txt", "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except FileNotFoundError:
    KNOWLEDGE_BASE = "داده‌ای یافت نشد."

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="سلام! من راهنمای گردشگری کردستان هستم. چطور می‌تونم کمکتون کنم؟"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    prompt = f"""شما یک راهنمای گردشگری متخصص برای استان کردستان هستید. 
فقط و فقط بر اساس اطلاعات زیر به سوالات پاسخ دهید. 
اگر پاسخ در اطلاعات زیر نبود، صادقانه بگویید که اطلاعاتی در این مورد ندارید.

اطلاعات مرجع:
{KNOWLEDGE_BASE}

سوال کاربر: {user_message}
"""
    try:
        response = client.chat.completions.create(
            model="google/gemini-flash-1.5",
            messages=[
                {"role": "system", "content": "You are a helpful tourism assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        bot_reply = response.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)
    except Exception as e:
        logging.error(f"Error: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="مشکلی پیش آمد. بعداً تلاش کنید.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    PORT = int(os.environ.get("PORT", 10000))
    URL = os.environ.get("RENDER_EXTERNAL_URL")
    
    if URL:
        # این بخش وب‌سرور رو باز می‌کنه تا Render راضی بشه
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=os.environ.get("TELEGRAM_TOKEN"),
            webhook_url=f"{URL}/{os.environ.get('TELEGRAM_TOKEN')}"
        )
    else:
        application.run_polling()
