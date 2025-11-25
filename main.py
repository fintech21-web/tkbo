import os
import threading
from flask import Flask, send_from_directory, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")

# Your Render domain (Webhook URL)
WEBHOOK_URL = "https://tkbo.onrender.com/webhook"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር የመመዝገቢያ ክፍያዎን 3420 ብር ይክፈሉ። "
        "ለመክፈል ይህን ይጫኑ /pay."
    )


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Your static image hosted by Render
    image_url = "https://tkbo.onrender.com/receipt"

    await update.message.reply_photo(
        photo=image_url,
        caption="💰 *የመክፈያ መመሪያ:*",
        parse_mode="Markdown"
    )

    message = (
        "እባክህ ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ሸጋው ታምሩ ተመስገን\n"
        "💳 የአካውንት ቁጥር: 567592816011\n"
        "🏦 የባንክ ስም: ዳሽን ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በ @bkuelmis ይላኩ።"
    )

    await update.message.reply_text(message, parse_mode="Markdown")


# --------------- FLASK APP (Webhook Endpoint + Static Image) ---------------
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running via webhook!"


# Serve your image file from /static
@flask_app.route("/receipt")
def serve_receipt():
    return send_from_directory("static", "receipt.png")


# Telegram sends updates HERE
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app.bot)
    app.update_queue.put_nowait(update)
    return "OK", 200


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)


# Run Flask in background thread
threading.Thread(target=run_flask, daemon=True).start()


# ---------------- TELEGRAM APP (Webhook Mode) ----------------
print("Starting Telegram bot in WEBHOOK MODE...")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pay", pay))

# Remove old polling and set webhook instead
async def set_webhook():
    await app.bot.set_webhook(WEBHOOK_URL)

import asyncio
asyncio.get_event_loop().run_until_complete(set_webhook())
