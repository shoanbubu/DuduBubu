import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import Forbidden
from flask import Flask  # Added for Render compatibility
import threading

# Flask app for Render's port requirement
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram bot is running!"

# Your existing bot code
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@Btec2025"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("សូមបញ្ចេញមតិយោបល់ ឬមានសំណូមពរដោយប្រកាន់ភ្ជាប់ក្រមសីលធម៌!")
    except Forbidden:
        print("Bot was blocked by the user")

# [Keep all your existing handler functions unchanged...]

def run_bot():
    if not TOKEN:
        print("❌ Error: Bot token is missing! Set TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app_bot.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app_bot.add_handler(MessageHandler(filters.ATTACHMENT, handle_document))

    print("✅ Bot is running...")
    app_bot.run_polling()

if __name__ == "__main__":
    # Start bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Start Flask server (required for Render)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
