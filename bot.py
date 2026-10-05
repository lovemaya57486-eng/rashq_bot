import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


TOKEN = os.getenv("BOT_TOKEN")


# -------------------------
# صفحة فحص Render
# -------------------------

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# -------------------------
# القائمة الرئيسية
# -------------------------

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛒 طلب خدمة", callback_data="order"),
            InlineKeyboardButton("📦 طلباتي", callback_data="orders")
        ],
        [
            InlineKeyboardButton("💳 الرصيد والمحفظة", callback_data="wallet"),
            InlineKeyboardButton("🛍️ الخدمات", callback_data="services")
        ],
        [
            InlineKeyboardButton("🔥 العروض", callback_data="offers"),
            InlineKeyboardButton("💰 الأسعار", callback_data="prices")
        ],
        [
            InlineKeyboardButton("⭐ نقاطي", callback_data="points"),
            InlineKeyboardButton("➕ شحن الرصيد", callback_data="deposit")
        ],
        [
            InlineKeyboardButton("🎁 المكافآت", callback_data="rewards"),
            InlineKeyboardButton("👤 حسابي", callback_data="account")
        ],
        [
            InlineKeyboardButton("📊 إحصائياتي", callback_data="stats"),
            InlineKeyboardButton("📞 الدعم الفني", callback_data="support")
        ],
        [
            InlineKeyboardButton("📢 الأخبار والتحديثات", callback_data="news"),
            InlineKeyboardButton("ℹ️ معلومات البوت", callback_data="info")
        ],
    ])


# -------------------------
# زر الرئيسية
# -------------------------

def home_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")]
    ])


# -------------------------
# أمر البداية
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "صديقي"

    text = (
        f"👋 أهلاً {name}!\n\n"
        "🤖 أهلاً بك في بوت الخدمات والرشق.\n\n"
        "اختر القسم الذي تريد الدخول إليه 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard()
    )


# -------------------------
# الأزرار
# -------------------------

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "home":
        await query.edit_message_text(
            "🏠 القائمة الرئيسية\n\nاختر القسم المطلوب 👇",
            reply_markup=main_keyboard()
        )
        return

    pages = {

        "orders":
            "📦 طلباتي\n\n"
            "لا توجد طلبات حتى الآن.\n\n"
            "🛒 يمكنك إنشاء طلب جديد من زر «طلب خدمة».",

        "wallet":
            "💳 الرصيد والمحفظة\n\n"
            "💰 الرصيد الحالي: 0.00\n"
            "📥 إجمالي الإيداعات: 0.00\n"
            "📤 إجمالي المصروفات: 0.00",

        "services":
            "🛍️ الخدمات\n\n"
            "📸 Instagram\n"
            "🎵 TikTok\n"
            "✈️ Telegram\n"
            "▶️ YouTube\n\n"
            "سيتم إضافة الخدمات والأسعار الفعلية لاحقًا.",

        "offers":
            "🔥 العروض والخصومات\n\n"
            "لا توجد عروض حالياً.\n\n"
            "📢 تابع الأخبار لمعرفة العروض الجديدة.",

        "prices":
            "💰 الأسعار\n\n"
            "سيتم عرض أسعار الخدمات بعد ربط مزود الخدمات.",

        "points":
            "⭐ نقاطي\n\n"
            "رصيد نقاطك الحالي: 0 نقطة\n\n"
            "🎁 اجمع النقاط واستبدلها بالمكافآت لاحقًا.",

        "deposit":
            "➕ شحن الرصيد\n\n"
            "💳 طرق الدفع سيتم إضافتها لاحقًا.\n\n"
            "سيظهر هنا نظام الشحن والتحويلات.",

        "rewards":
            "🎁 المكافآت\n\n"
            "لا توجد مكافآت متاحة حالياً.",

        "account":
            f"👤 حسابي\n\n"
            f"الاسم: {query.from_user.full_name}\n"
            f"🆔 Telegram ID: {query.from_user.id}\n\n"
            "💳 الرصيد: 0.00\n"
            "⭐ النقاط: 0",

        "stats":
            "📊 إحصائياتي\n\n"
            "📦 عدد الطلبات: 0\n"
            "💰 إجمالي المصروف: 0.00\n"
            "⭐ النقاط: 0\n"
            "✅ الطلبات المكتملة: 0",

        "support":
            "📞 الدعم الفني\n\n"
            "إذا واجهت أي مشكلة أو لديك استفسار،\n"
            "سيتم إضافة نظام الدعم والتذاكر هنا.",

        "news":
            "📢 الأخبار والتحديثات\n\n"
            "لا توجد أخبار أو تحديثات حالياً.",

        "info":
            "ℹ️ معلومات البوت\n\n"
            "🤖 بوت خدمات ورشق\n"
            "🛒 طلب الخدمات\n"
            "💳 إدارة الرصيد\n"
            "⭐ نظام النقاط\n"
            "🎁 نظام المكافآت\n\n"
            "🚀 النظام قابل للتطوير وإضافة الخدمات.",

        "order":
            "🛒 طلب خدمة\n\n"
            "اختر المنصة التي تريد الطلب منها 👇"
    }

    if data == "order":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📸 Instagram", callback_data="instagram")],
            [InlineKeyboardButton("🎵 TikTok", callback_data="tiktok")],
            [InlineKeyboardButton("✈️ Telegram", callback_data="telegram")],
            [InlineKeyboardButton("▶️ YouTube", callback_data="youtube")],
            [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")]
        ])

        await query.edit_message_text(
            "🛒 طلب خدمة\n\nاختر المنصة:",
            reply_markup=keyboard
        )
        return

    if data in ["instagram", "tiktok", "telegram", "youtube"]:
        names = {
            "instagram": "📸 Instagram",
            "tiktok": "🎵 TikTok",
            "telegram": "✈️ Telegram",
            "youtube": "▶️ YouTube"
        }

        await query.edit_message_text(
            f"{names[data]}\n\n"
            "🔧 الخدمات الخاصة بهذه المنصة سيتم إضافتها لاحقًا.\n\n"
            "نحن الآن نجهز واجهة البوت وربط الخدمات.",
            reply_markup=home_keyboard()
        )
        return

    if data in pages:
        await query.edit_message_text(
            pages[data],
            reply_markup=home_keyboard()
        )


# -------------------------
# تشغيل البوت
# -------------------------

def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN غير موجود في Environment Variables"
        )

    # تشغيل صفحة Render
    threading.Thread(
        target=start_health_server,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
