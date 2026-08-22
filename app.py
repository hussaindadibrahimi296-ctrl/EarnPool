import os
from flask import Flask

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEB_APP_URL = os.environ.get("WEB_APP_URL")


@app.route("/")
def home():
    return "EarnPool is running!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Open EarnPool",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ]

    message = """
<b>🌟 Welcome to EarnPool!</b>

🪙 Earn Telcoin by completing simple activities inside EarnPool.

💰 You can earn Telcoin through:
• 🎁 Daily rewards
• 📺 Watching available ads
• 📋 Completing tasks
• 👥 Inviting friends

<b>👥 Referral Rewards</b>

Invite your friends using your personal referral link.
When your referrals become active users and complete eligible activities, you can receive referral rewards according to the current EarnPool rules.

💎 Your Telcoin balance can be viewed anytime inside your account.

🚀 Start earning by opening EarnPool below!
"""

    await update.message.reply_text(
        message,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪙 Your current balance:\n\n0 Telcoin\n≈ $0.00"
    )


async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    bot_username = context.bot.username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    await update.message.reply_text(
        f"👥 <b>Your Referral</b>\n\n"
        f"Invite friends and earn Telcoin according to the current referral rules.\n\n"
        f"🔗 Your referral link:\n{referral_link}",
        parse_mode="HTML"
    )


async def account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👤 <b>Account</b>\n\n"
        "🪙 Balance: 0 Telcoin\n"
        "💵 Value: $0.00\n"
        "👥 Referrals: 0\n"
        "📋 Tasks completed: 0\n"
        "📺 Ads watched: 0",
        parse_mode="HTML"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ <b>EarnPool Help</b>\n\n"
        "/start — Open EarnPool\n"
        "/balance — Check your balance\n"
        "/referral — Get your referral link\n"
        "/account — View your account\n"
        "/help — Show help",
        parse_mode="HTML"
    )


async def run_bot():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    if not WEB_APP_URL:
        raise RuntimeError("WEB_APP_URL is not configured")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("referral", referral))
    application.add_handler(CommandHandler("account", account))
    application.add_handler(CommandHandler("help", help_command))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    print("EarnPool Telegram Bot is running!")

    import asyncio
    await asyncio.Event().wait()


@app.route("/start-bot")
def start_bot():
    import asyncio
    asyncio.run(run_bot())
    return "Bot started"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
