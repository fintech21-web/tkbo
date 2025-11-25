import os
import threading
from flask import Flask, send_from_directory
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር የመመዝገቢያ ክፍያዎን 3420 ብር ይክፈሉ። "
        "ለመክፈል ይህን ይጫኑ /pay."
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 🔥 Send your local Render-hosted image — always works in Ethiopia
    image_url = "https://tkbo.onrender.com/receipt"

    await update.message.reply_photo(
        photo=image_url,
        caption="💰 *የመክፈያ መመሪያ:*",
        parse_mode="Markdown"
    )

    # Then send the bank details
    message = (
        "እባክህ ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ሸጋው ታምሩ ተመስገን\n"
        "💳 የአካውንት ቁጥር: 567592816011\n"
        "🏦 የባንክ ስም: ዳሽን ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በ @bkuelmis ይላኩ።"
    )
    await update.message.reply_text(message, parse_mode="Markdown")


# --- Flask App to keep Render alive + Serve Image ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

# Route for your image
@flask_app.route('/receipt')
def serve_receipt():
    return send_from_directory("static", "receipt.png")


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()


# --- Start Telegram Bot ---
print("Starting Telegram bot...")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pay", pay))
app.run_polling()
