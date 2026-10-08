from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from database import init_database, seed_services


# =========================
# النصوص
# =========================

TEXTS = {
    "ar": {
        "home_title": "🏥 سمارت بايوميد لهندسة الأجهزة الطبية",
        "home": (
            "مرحباً بك في نظام سمارت بايوميد للخدمات الهندسية والطبية.\n\n"
            "يمكنك من خلال النظام:\n"
            "🔧 طلب صيانة\n"
            "🛒 شراء أجهزة طبية\n"
            "🔩 طلب قطع غيار\n"
            "🧠 استشارة هندسية\n"
            "📦 مشاهدة المخزون\n"
            "📋 متابعة الطلبات\n"
            "📞 التواصل مع المكتب\n"
            "📱 استخدام التطبيق\n\n"
            "اختر الخدمة من القائمة أدناه:"
        ),

        "purchase": (
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
        ),

        "maintenance": (
            "🔧 طلب صيانة\n\n"
            "يمكنك إرسال طلب صيانة لأحد الأجهزة الطبية.\n\n"
            "سيطلب منك النظام:\n"
            "• بيانات الجهاز\n"
            "• وصف العطل\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• الصور والمرفقات\n"
            "• الملاحظات الإضافية"
        ),

        "spare_parts": (
            "🔩 قطع الغيار\n\n"
            "يمكنك مشاهدة قطع الغيار المتوفرة "
            "وإرسال طلب شراء.\n\n"
            "سيطلب منك النظام:\n"
            "• بيانات العميل\n"
            "• قطعة الغيار المطلوبة\n"
            "• الكمية\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• الوصف والملاحظات"
        ),

        "consultation": (
            "🧠 الاستشارة الهندسية\n\n"
            "يمكنك إرسال طلب استشارة هندسية للمكتب.\n\n"
            "سيشمل الطلب:\n"
            "• نوع الاستشارة\n"
            "• شرح المشكلة\n"
            "• المرفقات\n"
            "• رقم الهاتف\n"
            "• الموقع\n"
            "• طريقة التواصل"
        ),

        "inventory": (
            "📦 المخزون\n\n"
            "يمكنك مشاهدة الأجهزة وقطع الغيار "
            "والأصناف المتوفرة في المخزون."
        ),

        "my_requests": (
            "📋 طلباتي\n\n"
            "يمكنك من هنا متابعة الطلبات الخاصة بك فقط.\n\n"
            "لا يستطيع المستخدم مشاهدة طلبات المستخدمين الآخرين."
        ),

        "search_request": (
            "🔎 البحث عن طلب\n\n"
            "يمكنك البحث عن طلبك باستخدام رقم الطلب."
        ),

        "contact": (
            "📞 تواصل مع المكتب\n\n"
            "سيتم هنا عرض وسائل التواصل مع مكتب "
            "سمارت بايوميد."
        ),

        "app": (
            "📱 استخدام التطبيق\n\n"
            "من هنا يمكنك فتح تطبيق "
            "Smart Biomed Office."
        ),

        "settings": (
            "⚙️ الإعدادات\n\n"
            "اختر اللغة التي تريد استخدامها:"
        ),

        "start_request": "🚀 بدء الطلب",
        "search": "🔎 البحث عن طلب",
        "open_app": "🚀 فتح التطبيق",
        "back": "↩️ رجوع",
        "arabic": "🇸🇦 العربية",
        "english": "🇬🇧 English",

        "coming_soon": (
            "🚧 هذه الوظيفة سيتم ربطها بالـMini App "
            "في الخطوة القادمة."
        ),

        "language_ar": "🇸🇦 تم اختيار اللغة العربية.",
        "language_en": "🇬🇧 English language selected.",
    },

    "en": {
        "home_title": "🏥 Smart Biomed Medical Equipment Engineering",
        "home": (
            "Welcome to Smart Biomed Engineering and Medical Services.\n\n"
            "Available services:\n"
            "🔧 Maintenance Request\n"
            "🛒 Medical Equipment Purchase\n"
            "🔩 Spare Parts\n"
            "🧠 Engineering Consultation\n"
            "📦 Inventory\n"
            "📋 My Requests\n"
            "📞 Contact Office\n"
            "📱 Use Application\n\n"
            "Please choose a service:"
        ),

        "purchase": (
            "🛒 Medical Equipment Purchase\n\n"
            "You can view available medical equipment "
            "and submit a purchase request.\n\n"
            "The system will ask for:\n"
            "• Customer information\n"
            "• Requested equipment\n"
            "• Quantity\n"
            "• Phone number\n"
            "• Location\n"
            "• Notes"
        ),

        "maintenance": (
            "🔧 Maintenance Request\n\n"
            "You can submit a maintenance request "
            "for a medical device.\n\n"
            "The system will ask for:\n"
            "• Device information\n"
            "• Problem description\n"
            "• Phone number\n"
            "• Location\n"
            "• Photos and attachments\n"
            "• Additional notes"
        ),

        "spare_parts": (
            "🔩 Spare Parts\n\n"
            "You can view available spare parts "
            "and submit a purchase request.\n\n"
            "The system will ask for:\n"
            "• Customer information\n"
            "• Required spare part\n"
            "• Quantity\n"
            "• Phone number\n"
            "• Location\n"
            "• Description and notes"
        ),

        "consultation": (
            "🧠 Engineering Consultation\n\n"
            "You can submit an engineering consultation request.\n\n"
            "The request includes:\n"
            "• Consultation type\n"
            "• Problem description\n"
            "• Attachments\n"
            "• Phone number\n"
            "• Location\n"
            "• Contact method"
        ),

        "inventory": (
            "📦 Inventory\n\n"
            "You can view available medical equipment "
            "and spare parts."
        ),

        "my_requests": (
            "📋 My Requests\n\n"
            "You can track your own requests here.\n\n"
            "Users cannot view other users' requests."
        ),

        "search_request": (
            "🔎 Search Request\n\n"
            "You can search for a request using its request number."
        ),

        "contact": (
            "📞 Contact Office\n\n"
            "Contact information for Smart Biomed Office "
            "will be available here."
        ),

        "app": (
            "📱 Use Application\n\n"
            "You can open the Smart Biomed Office application from here."
        ),

        "settings": (
            "⚙️ Settings\n\n"
            "Choose your preferred language:"
        ),

        "start_request": "🚀 Start Request",
        "search": "🔎 Search Request",
        "open_app": "🚀 Open Application",
        "back": "↩️ Back",
        "arabic": "🇸🇦 العربية",
        "english": "🇬🇧 English",

        "coming_soon": (
            "🚧 This feature will be connected to the Mini App "
            "in the next step."
        ),

        "language_ar": "🇸🇦 Arabic language selected.",
        "language_en": "🇬🇧 English language selected.",
    },
}


# =========================
# اللغة
# =========================

def get_language(context):
    return context.user_data.get("language", "ar")


# =========================
# القائمة الرئيسية
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lang = get_language(context)
    t = TEXTS[lang]

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 شراء الأجهزة الطبية" if lang == "ar"
                else "🛒 Medical Equipment",
                callback_data="purchase"
            ),
            InlineKeyboardButton(
                "🔧 طلب صيانة" if lang == "ar"
                else "🔧 Maintenance",
                callback_data="maintenance"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔩 قطع الغيار" if lang == "ar"
                else "🔩 Spare Parts",
                callback_data="spare_parts"
            ),
            InlineKeyboardButton(
                "🧠 الاستشارة الهندسية" if lang == "ar"
                else "🧠 Consultation",
                callback_data="consultation"
            ),
        ],
        [
            InlineKeyboardButton(
                "📦 المخزون" if lang == "ar"
                else "📦 Inventory",
                callback_data="inventory"
            ),
            InlineKeyboardButton(
                "📋 طلباتي" if lang == "ar"
                else "📋 My Requests",
                callback_data="my_requests"
            ),
        ],
        [
            InlineKeyboardButton(
                "📞 تواصل مع المكتب" if lang == "ar"
                else "📞 Contact Office",
                callback_data="contact"
            ),
        ],
        [
            InlineKeyboardButton(
                "📱 استخدام التطبيق" if lang == "ar"
                else "📱 Use Application",
                callback_data="app"
            ),
            InlineKeyboardButton(
                "⚙️ الإعدادات" if lang == "ar"
                else "⚙️ Settings",
                callback_data="settings"
            ),
        ],
    ]

    await send_or_edit(
        update,
        f"{t['home_title']}\n\n{t['home']}",
        InlineKeyboardMarkup(keyboard)
    )


# =========================
# إرسال رسالة أو تعديلها
# =========================

async def send_or_edit(update, text, markup):

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=markup
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=markup
        )


# =========================
# الأزرار
# =========================

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    lang = get_language(context)
    t = TEXTS[lang]

    # -------------------------
    # الخدمات
    # -------------------------

    if query.data in [
        "purchase",
        "maintenance",
        "spare_parts",
        "consultation"
    ]:

        keyboard = [
            [
                InlineKeyboardButton(
                    t["start_request"],
                    callback_data=f"start_{query.data}"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="back_home"
                )
            ],
        ]

        await query.edit_message_text(
            text=t[query.data],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # -------------------------
    # بدء الطلب
    # -------------------------

    elif query.data.startswith("start_"):

        await query.edit_message_text(
            text=t["coming_soon"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    # -------------------------
    # المخزون
    # -------------------------

    elif query.data == "inventory":

        keyboard = [
            [
                InlineKeyboardButton(
                    "👀 عرض المخزون" if lang == "ar"
                    else "👀 View Inventory",
                    callback_data="view_inventory"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="back_home"
                )
            ]
        ]

        await query.edit_message_text(
            text=t["inventory"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "view_inventory":

        await query.edit_message_text(
            text=(
                "📦 المخزون\n\n"
                "سيتم عرض الأصناف المتوفرة هنا."
                if lang == "ar"
                else
                "📦 Inventory\n\n"
                "Available items will be displayed here."
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    # -------------------------
    # طلباتي
    # -------------------------

    elif query.data == "my_requests":

        keyboard = [
            [
                InlineKeyboardButton(
                    t["search"],
                    callback_data="search_request"
                )
            ],
            [
                InlineKeyboardButton(
                    "📋 عرض طلباتي" if lang == "ar"
                    else "📋 View My Requests",
                    callback_data="view_my_requests"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="back_home"
                )
            ]
        ]

        await query.edit_message_text(
            text=t["my_requests"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "search_request":

        await query.edit_message_text(
            text=t["search_request"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🚀 بدء البحث" if lang == "ar"
                        else "🚀 Start Search",
                        callback_data="start_search"
                    )
                ],
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    elif query.data == "start_search":

        await query.edit_message_text(
            text=t["coming_soon"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    elif query.data == "view_my_requests":

        await query.edit_message_text(
            text=(
                "📋 لا توجد طلبات لعرضها حالياً."
                if lang == "ar"
                else
                "📋 There are no requests to display yet."
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    # -------------------------
    # التواصل
    # -------------------------

    elif query.data == "contact":

        await query.edit_message_text(
            text=t["contact"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    # -------------------------
    # التطبيق
    # -------------------------

    elif query.data == "app":

        await query.edit_message_text(
            text=t["app"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["open_app"],
                        callback_data="open_app"
                    )
                ],
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    elif query.data == "open_app":

        await query.edit_message_text(
            text=t["coming_soon"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="back_home"
                    )
                ]
            ])
        )

    # -------------------------
    # الإعدادات
    # -------------------------

    elif query.data == "settings":

        keyboard = [
            [
                InlineKeyboardButton(
                    t["arabic"],
                    callback_data="language_ar"
                ),
                InlineKeyboardButton(
                    t["english"],
                    callback_data="language_en"
                )
            ],
            [
                InlineKeyboardButton(
                    t["back"],
                    callback_data="back_home"
                )
            ]
        ]

        await query.edit_message_text(
            text=t["settings"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # -------------------------
    # اللغة العربية
    # -------------------------

    elif query.data == "language_ar":

        context.user_data["language"] = "ar"

        t = TEXTS["ar"]

        await query.answer("🇸🇦 العربية")

        await show_home_from_callback(query, "ar")

    # -------------------------
    # اللغة الإنجليزية
    # -------------------------

    elif query.data == "language_en":

        context.user_data["language"] = "en"

        t = TEXTS["en"]

        await query.answer("🇬🇧 English")

        await show_home_from_callback(query, "en")

    # -------------------------
    # الرجوع
    # -------------------------

    elif query.data == "back_home":

        await show_home_from_callback(query, lang)


# =========================
# إظهار القائمة الرئيسية
# =========================

async def show_home_from_callback(query, lang):

    t = TEXTS[lang]

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 شراء الأجهزة الطبية" if lang == "ar"
                else "🛒 Medical Equipment",
                callback_data="purchase"
            ),
            InlineKeyboardButton(
                "🔧 طلب صيانة" if lang == "ar"
                else "🔧 Maintenance",
                callback_data="maintenance"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔩 قطع الغيار" if lang == "ar"
                else "🔩 Spare Parts",
                callback_data="spare_parts"
            ),
            InlineKeyboardButton(
                "🧠 الاستشارة الهندسية" if lang == "ar"
                else "🧠 Consultation",
                callback_data="consultation"
            ),
        ],
        [
            InlineKeyboardButton(
                "📦 المخزون" if lang == "ar"
                else "📦 Inventory",
                callback_data="inventory"
            ),
            InlineKeyboardButton(
                "📋 طلباتي" if lang == "ar"
                else "📋 My Requests",
                callback_data="my_requests"
            ),
        ],
        [
            InlineKeyboardButton(
                "📞 تواصل مع المكتب" if lang == "ar"
                else "📞 Contact Office",
                callback_data="contact"
            ),
        ],
        [
            InlineKeyboardButton(
                "📱 استخدام التطبيق" if lang == "ar"
                else "📱 Use Application",
                callback_data="app"
            ),
            InlineKeyboardButton(
                "⚙️ الإعدادات" if lang == "ar"
                else "⚙️ Settings",
                callback_data="settings"
            ),
        ],
    ]

    await query.edit_message_text(
        text=f"{t['home_title']}\n\n{t['home']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# تشغيل البوت
# =========================

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
