import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import Forbidden

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Telegram Bot is Running", 200

# Bot Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@Btec2025"

# Handler functions must be defined before run_bot()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("សូមបញ្ចេញមតិយោបល់ ឬមានសំណូមពរដោយប្រកាន់ភ្ជាប់ក្រមសីលធម៌!")
    except Forbidden:
        print("Bot was blocked by the user")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text:
        try:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=f"📩 សំបុត្រ:\n{text}")
        except Exception as e:
            await update.message.reply_text("❌ Failed to send the message. Please try again.")
            print(f"Error sending message: {e}")

# [Keep all your other handler functions here...]

def run_bot():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.ATTACHMENT, handle_document))
    
    print("🟢 Bot is now polling...")
    application.run_polling()

if __name__ == "__main__":
    # Start bot in a daemon thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
