import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛒 طلب خدمة", callback_data="order"),
            InlineKeyboardButton("📦 طلباتي", callback_data="orders"),
        ],
        [
            InlineKeyboardButton("💳 الرصيد والمحفظة", callback_data="wallet"),
            InlineKeyboardButton("🛍️ الخدمات", callback_data="services"),
        ],
        [
            InlineKeyboardButton("🔥 العروض", callback_data="offers"),
            InlineKeyboardButton("💰 الأسعار", callback_data="prices"),
        ],
        [
            InlineKeyboardButton("⭐ نقاطي", callback_data="points"),
            InlineKeyboardButton("➕ شحن الرصيد", callback_data="deposit"),
        ],
        [
            InlineKeyboardButton("🎁 المكافآت", callback_data="rewards"),
            InlineKeyboardButton("👤 حسابي", callback_data="account"),
        ],
        [
            InlineKeyboardButton("📊 إحصائياتي", callback_data="stats"),
            InlineKeyboardButton("📞 الدعم الفني", callback_data="support"),
        ],
        [
            InlineKeyboardButton("📢 الأخبار والتحديثات", callback_data="news"),
            InlineKeyboardButton("ℹ️ معلومات البوت", callback_data="info"),
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "صديقي"

    text = (
        f"👋 أهلاً {name}!\n\n"
        "🤖 أهلاً بك في بوت الخدمات.\n"
        "اختر من القائمة ما تريد القيام به 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard()
    )


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
        "orders": "📦 طلباتي\n\nلا توجد طلبات حتى الآن.",
        "wallet": "💳 الرصيد والمحفظة\n\n💰 الرصيد: 0.00\n📥 الإيداعات: 0.00\n📤 المصروفات: 0.00",
        "services": "🛍️ الخدمات\n\n📸 Instagram\n🎵 TikTok\n✈️ Telegram\n▶️ YouTube",
        "offers": "🔥 العروض والخصومات\n\nلا توجد عروض حاليًا.",
        "prices": "💰 الأسعار\n\nسيتم إضافة الأسعار بعد ربط مزود الخدمات.",
        "points": "⭐ نقاطي\n\nنقاطك الحالية: 0",
        "deposit": "➕ شحن الرصيد\n\nسيتم إضافة طرق الدفع لاحقًا.",
        "rewards": "🎁 المكافآت\n\nلا توجد مكافآت حاليًا.",
        "account": (
            f"👤 حسابي\n\n"
            f"الاسم: {query.from_user.full_name}\n"
            f"🆔 ID: {query.from_user.id}"
        ),
        "stats": "📊 إحصائياتي\n\n📦 الطلبات: 0\n💰 المصروف: 0.00\n⭐ النقاط: 0",
        "support": "📞 الدعم الفني\n\nسيتم إضافة نظام الدعم والتذاكر لاحقًا.",
        "news": "📢 الأخبار والتحديثات\n\nلا توجد تحديثات حاليًا.",
        "info": "ℹ️ معلومات البوت\n\nبوت خدمات ورشق قابل للتخصيص.",
        "order": (
            "🛒 طلب خدمة\n\n"
            "اختر المنصة التي تريد الطلب منها:\n\n"
            "📸 Instagram\n"
            "🎵 TikTok\n"
            "✈️ Telegram\n"
            "▶️ YouTube"
        ),
    }

    if data in pages:
        await query.edit_message_text(
            pages[data],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")]
            ])
        )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN غير موجود. أضفه في Environment Variables على Render."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()