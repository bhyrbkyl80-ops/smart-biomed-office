from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN
from database import init_database, seed_services


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك في بوت الخدمات 👋\n\n"
        "سيتم تجهيز الخدمات لك قريباً."
    )


def main():
    init_database()
    seed_services()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
