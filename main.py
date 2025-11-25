import os
from flask import Flask, request, send_from_directory
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., "https://tkbo.onrender.com/telegram_webhook"

bot = Bot(token=TOKEN)
app = Flask(__name__)

# --- Telegram Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር የመመዝገቢያ ክፍያዎን 3420 ብር ይክፈሉ። "
        "ለመክፈል ይህን ይጫኑ /pay."
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = "https://tkbo.onrender.com/receipt"
    await update.message.reply_photo(photo=image_url, caption="💰 *የመክፈያ መመሪያ:*", parse_mode="Markdown")
    message = (
        "እባክህ ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ሸጋው ታምሩ ተመስገን\n"
        "💳 የአካውንት ቁጥር: 567592816011\n"
        "🏦 የባንክ ስም: ዳሽን ባንክ\n\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በ @bkuelmis ይላኩ።"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# --- Dispatcher ---
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pay", pay))

dispatcher: Dispatcher = application.dispatcher

# --- Flask Routes ---
@app.route('/')
def home():
    return "Bot is running!"

@app.route('/receipt')
def serve_receipt():
    return send_from_directory("static", "receipt.png")

@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.run_async(dispatcher.process_update(update))
    return "OK"

# --- Set Webhook on Start ---
@app.before_first_request
def set_webhook():
    bot.delete_webhook()  # remove old webhook if exists
    bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
