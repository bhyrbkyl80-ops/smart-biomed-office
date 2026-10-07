from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from database import init_database, seed_services


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🛒 شراء الأجهزة الطبية", callback_data="purchase"),
            InlineKeyboardButton("🔧 طلب صيانة", callback_data="maintenance"),
        ],
        [
            InlineKeyboardButton("🔩 قطع الغيار", callback_data="spare_parts"),
            InlineKeyboardButton("🧠 الاستشارة الهندسية", callback_data="consultation"),
        ],
        [
            InlineKeyboardButton("📦 المخزون", callback_data="inventory"),
            InlineKeyboardButton("📋 طلباتي", callback_data="my_requests"),
        ],
        [
            InlineKeyboardButton("📞 تواصل مع المكتب", callback_data="contact"),
        ],
        [
            InlineKeyboardButton("📱 استخدام التطبيق", callback_data="app"),
            InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🏥 سمارت بايوميد لهندسة الأجهزة الطبية\n\n"
        "مرحباً بك في نظام سمارت بايوميد للخدمات الهندسية والطبية.\n\n"
        "يمكنك من خلال النظام:\n"
        "🔧 طلب صيانة\n"
        "🛒 شراء أجهزة طبية\n"
        "🔩 طلب قطع غيار\n"
        "🧠 استشارة هندسية\n"
        "📦 مشاهدة المخزون\n"
        "📞 التواصل مع المكتب\n"
        "📱 استخدام التطبيق\n\n"
        "اختر الخدمة من القائمة أدناه:",
        reply_markup=reply_markup
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "purchase":
        await query.message.reply_text(
            "🛒 شراء الأجهزة الطبية\n\n"
            "سيتم تجهيز نموذج شراء الأجهزة الطبية قريباً."
        )

    elif query.data == "maintenance":
        await query.message.reply_text(
            "🔧 طلب صيانة\n\n"
            "سيتم تجهيز نموذج طلب الصيانة قريباً."
        )

    elif query.data == "spare_parts":
        await query.message.reply_text(
            "🔩 قطع الغيار\n\n"
            "سيتم تجهيز نموذج طلب قطع الغيار قريباً."
        )

    elif query.data == "consultation":
        await query.message.reply_text(
            "🧠 الاستشارة الهندسية\n\n"
            "سيتم تجهيز نموذج الاستشارة الهندسية قريباً."
        )

    elif query.data == "inventory":
        await query.message.reply_text(
            "📦 المخزون\n\n"
            "سيتم عرض الأجهزة وقطع الغيار المتوفرة هنا."
        )

    elif query.data == "my_requests":
        await query.message.reply_text(
            "📋 طلباتي\n\n"
            "سيتم عرض طلباتك هنا."
        )

    elif query.data == "contact":
        await query.message.reply_text(
            "📞 تواصل مع المكتب\n\n"
            "سيتم تجهيز بيانات التواصل قريباً."
        )

    elif query.data == "app":
        await query.message.reply_text(
            "📱 استخدام التطبيق\n\n"
            "سيتم فتح تطبيق Smart Biomed Office هنا."
        )

    elif query.data == "settings":
        await query.message.reply_text(
            "⚙️ الإعدادات\n\n"
            "اختر اللغة التي تريد استخدامها."
        )


def main():

    init_database()
    seed_services()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        CallbackQueryHandler(button_click)
    )

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
