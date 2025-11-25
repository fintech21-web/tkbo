import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")

# Replace with your direct .jpg or .png URL
PHOTO_URL = "https://i.imgur.com/yKNBqbk.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በ ስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር የመመዝገቢያ ክፍያዎን ይክፈሉ። "
        "ለመክፈል ይህን ይጫኑ /pay."
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Send image first
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption="💰 *የመክፈያ መመሪያ:*",
        parse_mode="Markdown"
    )

    # Then send text
    message = (
        "እባክህ ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ዶ/ር አለምነህ ከፍያለው\n"
        "💳 የአካውንት: 1000489297275\n"
        "🏦 የባንክ ስም: የኢትዮጵያ ንግድ ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በ @bkuelmis ይላኩ።"
    )
    await update.message.reply_text(message, parse_mode="Markdown")


# --- Flask App to keep Render alive ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

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
