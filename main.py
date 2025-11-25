import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")
PHOTO_URL = "https://i.imgur.com/yKNBqbk.png"   # <<--- Replace with .jpg/.png link

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ  በ ስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር የ መመዝገቢያ ክፍያዎን 3420 ብር  ይክፈሉ። "
        "ለመክፈል ይህን ይጫኑ /pay."
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # --- Send Photo First ---
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption="💰 *የመክፈያ መመሪያ:*",
        parse_mode="Markdown"
    )

    # --- Then Send Payment Details ---
    message = (
        "እባክህ ክፍያዎን ከታች በተቀመጠው የ ባንክ አካውንት ይላኩ:\n\n"
        "🏦 የ አካውንት ስም : ዶ/ር ሸጋው ታምሩ ተመስገን\n"
        "💳 አካውንት ቁጥር : 567592816011\n"
        "🏦 የ ባንክ ስም : ዳሽን ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙኝ በዚህ የ telegram Link @bkuelmis ይላኩ።"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# --- Flask App (for Render uptime) ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in a background thread
threading.Thread(target=run_flask, daemon=True).start()

# --- Start Telegram Bot ---
print("Starting Telegram bot...")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pay", pay))
app.run_polling()
