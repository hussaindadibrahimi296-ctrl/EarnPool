import os
import asyncio
import threading

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

💰 Ways to earn:
• 🎁 Daily Reward
• 📺 Watch available ads
• 📋 Complete tasks
• 👥 Invite friends

<b>👥 Earn with Referrals</b>

Invite your friends using your personal referral link.
When eligible referral activities are completed, you can receive Telcoin according to the current EarnPool rules.

💎 Your balance and earnings can be checked anytime.

🚀 Open EarnPool and start earning Telcoin!
"""

    await update.message.reply_text(
        message,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪙 <b>Your Balance</b>\n\n"
        "0 Telcoin\n"
        "≈ $0.00",
        parse_mode="HTML"
    )


async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_username = context.bot.username

    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    await update.message.reply_text(
        f"👥 <b>Your Referral</b>\n\n"
        f"Invite friends and earn Telcoin according to the current rules.\n\n"
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


async def start_telegram_bot():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN is missing")
        return

    if not WEB_APP_URL:
        print("ERROR: WEB_APP_URL is missing")
        return

    bot_app = Application.builder().token(BOT_TOKEN).build()

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("balance", balance))
    bot_app.add_handler(CommandHandler("referral", referral))
    bot_app.add_handler(CommandHandler("account", account))
    bot_app.add_handler(CommandHandler("help", help_command))

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()

    print("EarnPool Telegram Bot is running!")

    while True:
        await asyncio.sleep(3600)


def run_bot():
    asyncio.run(start_telegram_bot())


if BOT_TOKEN and WEB_APP_URL:
    bot_thread = threading.Thread(
        target=run_bot,
        daemon=True
    )
    bot_thread.start()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
