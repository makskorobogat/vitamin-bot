import os
import datetime
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

last_answer_date = None  # запоминаем день

praise_yes = [
    "Умничка 😘 Горжусь тобой 💖",
    "Милашка ты, ать по головушке тебя 🌸",
    "Вот так держать 💪❤️",
    "Заюшка Юляшка так держать! ☀️"
]

praise_no = [
    "Ничего страшного, завтра обязательно надо принять 💊❤️",
    "Главное — не забыть завтра, я напомню 😘",
    "Ты всё равно умничка 🌷, напомню завтра"
]


def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Да, приняла", callback_data="yes")],
        [InlineKeyboardButton("❌ Пока нет, приму сегодня позже или уже завтра", callback_data="no")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Привет 💖 Я бот-напоминалка про витамин D ☀️\nТы сегодня уже приняла витаминку?"
    await update.message.reply_text(text, reply_markup=get_keyboard())


async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    global last_answer_date
    today = datetime.date.today()

    if last_answer_date == today:
        return  # уже ответила сегодня

    text = "💊 Ты сегодня уже приняла витамин D, Юляшка?"
    await context.bot.send_message(chat_id=CHAT_ID, text=text, reply_markup=get_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_answer_date
    query = update.callback_query
    await query.answer()

    today = datetime.date.today()

    if query.data == "yes":
        last_answer_date = today
        await query.edit_message_text(random.choice(praise_yes))

    elif query.data == "no":
        last_answer_date = today
        await query.edit_message_text(random.choice(praise_no))


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    scheduler = BackgroundScheduler(timezone="Europe/Berlin")
    scheduler.add_job(daily_reminder, "cron", hour=19, minute=0)
    scheduler.start()

    app.run_polling()


if __name__ == "__main__":
    main()
