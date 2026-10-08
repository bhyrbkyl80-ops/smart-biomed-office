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
            InlineKeyboardButton(
                "🛒 شراء الأجهزة الطبية",
                callback_data="purchase"
            ),
            InlineKeyboardButton(
                "🔧 طلب صيانة",
                callback_data="maintenance"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔩 قطع الغيار",
                callback_data="spare_parts"
            ),
            InlineKeyboardButton(
                "🧠 الاستشارة الهندسية",
                callback_data="consultation"
            ),
        ],
        [
            InlineKeyboardButton(
                "📦 المخزون",
                callback_data="inventory"
            ),
            InlineKeyboardButton(
                "📋 طلباتي",
                callback_data="my_requests"
            ),
        ],
        [
            InlineKeyboardButton(
                "📞 تواصل مع المكتب",
                callback_data="contact"
            ),
        ],
        [
            InlineKeyboardButton(
                "📱 استخدام التطبيق",
                callback_data="app"
            ),
            InlineKeyboardButton(
                "⚙️ الإعدادات",
                callback_data="settings"
            ),
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

    if query.data == "maintenance":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 بدء طلب الصيانة",
                    callback_data="start_maintenance"
                )
            ],
            [
                InlineKeyboardButton(
                    "↩️ رجوع",
                    callback_data="back_home"
                )
            ],
        ]

        await query.message.reply_text(
            "🔧 طلب صيانة\n\n"
            "يمكنك من خلال هذه الخدمة إرسال طلب صيانة "
            "لأحد الأجهزة الطبية.\n\n"
            "سيطلب منك النظام:\n"
            "• بيانات الجهاز\n"
            "• وصف العطل\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• الصور والمرفقات\n"
            "• أي ملاحظات إضافية\n\n"
            "بعد إرسال الطلب سيتم إنشاء رقم خاص لطلبك "
            "وإرساله إلى المكتب لمراجعته.\n\n"
            "اضغط على «🚀 بدء طلب الصيانة» للمتابعة.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "purchase":

        await query.message.reply_text(
            "🛒 شراء الأجهزة الطبية\n\n"
            "يمكنك مشاهدة الأجهزة الطبية المتوفرة "
            "وإرسال طلب شراء.\n\n"
            "سيطلب منك النظام:\n"
            "• بيانات العميل\n"
            "• الجهاز المطلوب\n"
            "• الكمية\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• الملاحظات"
        )

    elif query.data == "spare_parts":

        await query.message.reply_text(
            "🔩 قطع الغيار\n\n"
            "يمكنك مشاهدة قطع الغيار المتوفرة "
            "وإرسال طلب شراء.\n\n"
            "سيطلب منك النظام:\n"
            "• بيانات العميل\n"
            "• قطعة الغيار المطلوبة\n"
            "• الكمية\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• الوصف أو الملاحظات"
        )

    elif query.data == "consultation":

        await query.message.reply_text(
            "🧠 الاستشارة الهندسية\n\n"
            "يمكنك إرسال طلب استشارة هندسية للمكتب.\n\n"
            "سيشمل الطلب:\n"
            "• نوع الاستشارة\n"
            "• شرح المشكلة\n"
            "• المرفقات\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• طريقة التواصل"
        )

    elif query.data == "inventory":

        await query.message.reply_text(
            "📦 المخزون\n\n"
            "يمكنك من هنا مشاهدة الأجهزة وقطع الغيار "
            "والأصناف المتوفرة في المخزون."
        )

    elif query.data == "my_requests":

        await query.message.reply_text(
            "📋 طلباتي\n\n"
            "هنا ستظهر الطلبات الخاصة بك فقط، "
            "ولا يستطيع المستخدم مشاهدة طلبات المستخدمين الآخرين."
        )

    elif query.data == "contact":

        await query.message.reply_text(
            "📞 تواصل مع المكتب\n\n"
            "سيتم هنا عرض وسائل التواصل مع مكتب "
            "سمارت بايوميد."
        )

    elif query.data == "app":

        await query.message.reply_text(
            "📱 استخدام التطبيق\n\n"
            "من هنا سيتم فتح تطبيق "
            "Smart Biomed Office."
        )

    elif query.data == "settings":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🇸🇦 العربية",
                    callback_data="language_ar"
                ),
                InlineKeyboardButton(
                    "🇬🇧 English",
                    callback_data="language_en"
                ),
            ]
        ]

        await query.message.reply_text(
            "⚙️ الإعدادات\n\n"
            "اختر اللغة التي تريد استخدامها:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "start_maintenance":

        await query.message.reply_text(
            "🚀 سيتم فتح نموذج طلب الصيانة هنا.\n\n"
            "في الخطوة القادمة سنربطه بالـMini App."
        )

    elif query.data == "back_home":

        await start(update, context)

    elif query.data == "language_ar":

        await query.message.reply_text(
            "🇸🇦 تم اختيار اللغة العربية."
        )

    elif query.data == "language_en":

        await query.message.reply_text(
            "🇬🇧 English language selected."
        )


def main():

    init_database()
    seed_services()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_click)
    )

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
