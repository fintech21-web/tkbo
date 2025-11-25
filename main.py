import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")

# Telegram file_id for the receipt image
FILE_ID = "AgACAgQAAxkBAAMbaSWTUbtSyaaO4nk7uY39DDptUOAAAsMLaxvFeSlRKhnYtBpPTJMBAAMCAAN5AAM2BA"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በ ስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር የመመዝገቢያ 3,420 ብር ይክፈሉ። "
        "ለመክፈል ይህን ይጫኑ /pay."
    )


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send image using Telegram file_id
    await update.message.reply_photo(
        photo=FILE_ID,
        caption=" *የተመደበሎት አምባሳደር ወይም ህጋዊ ወኪል:*",
        parse_mode="Markdown"
    )

    # Then send text instructions
    message = (
        "💰 የመክፈያ መመሪያ:\n\n"
        "ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ሸጋው ታምሩ ተመስገን\n"
        "💳 የአካውንት: 567592816011\n"
        "🏦 የባንክ ስም: ዳሽን ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በ @bkuelmis ይላኩ።"
    )
    await update.message.reply_text(message, parse_mode="Markdown")


# --- Get file_id command ---
async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        largest = update.message.photo[-1]  # get the largest version
        await update.message.reply_text(f"File ID: {largest.file_id}")
    else:
        await update.message.reply_text("እባክህ አንድ ፎቶ ላክ።")


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
app.add_handler(CommandHandler("get_file_id", get_file_id))
app.add_handler(MessageHandler(filters.PHOTO, get_file_id))  # optional auto-get file_id on photo

app.run_polling()
