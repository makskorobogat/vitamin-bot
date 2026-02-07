import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# Сообщение напоминания
REMINDER_TEXT = "💊 Не забудь выпить витамин D! ❤️"

async def remind(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ Выпила", callback_data="done")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=CHAT_ID, text=REMINDER_TEXT, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "done":
        await query.edit_message_text(text="Умничка! 🌞 Горд за тебя ❤️")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я буду напоминать тебе о витамине D ☀️")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    # Планировщик
    scheduler = BackgroundScheduler(timezone="Europe/Berlin")  # подставь свой часовой пояс
    scheduler.add_job(remind, "cron", hour=11, minute=0, args=[app.bot])
    scheduler.start()

    app.run_polling()

if __name__ == "__main__":
    main()
