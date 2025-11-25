import os
from flask import Flask, send_from_directory, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher

# --- Environment Variables ---
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://tkbo.onrender.com/telegram_webhook")
PORT = int(os.environ.get("PORT", 10000))

# --- Flask App Setup ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

# Serve the receipt image
@flask_app.route('/receipt')
def serve_receipt():
    return send_from_directory("static", "receipt.png")

# Telegram webhook endpoint
@flask_app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

# --- Telegram Bot Setup ---
bot = Bot(token=TOKEN)
app = ApplicationBuilder().token(TOKEN).build()
dispatcher = app.dispatcher  # Used for Flask webhook processing

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር "
        "የመመዝገቢያ ክፍያዎን 3420 ብር ይክፈሉ። ለመክፈል ይህን ይጫኑ /pay."
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = f"{WEBHOOK_URL.replace('/telegram_webhook','')}/receipt"
    
    # Send receipt image
    await update.message.reply_photo(
        photo=image_url,
        caption="💰 *የመክፈያ መመሪያ:*",
        parse_mode="Markdown"
    )

    # Send bank details
    message = (
        "እባክህ ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ሸጋው ታምሩ ተመስገን\n"
        "💳 የአካውንት ቁጥር: 567592816011\n"
        "🏦 የባንክ ስም: ዳሽን ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በ @bkuelmis ይላኩ።"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pay", pay))

# --- Delete any existing webhook first ---
bot.delete_webhook()

# --- Run Flask App ---
if __name__ == "__main__":
    print("Starting Flask app and webhook...")
    bot.set_webhook(url=WEBHOOK_URL)
    flask_app.run(host="0.0.0.0", port=PORT)
