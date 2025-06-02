import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Initialize Flask app for Render's port requirement
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Telegram Bot is Running", 200

# Bot Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@Btec2025"

# [Keep all your existing handler functions...]

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
    
    # Start Flask server using Gunicorn if available
    port = int(os.environ.get("PORT", 10000))
    if 'gunicorn' not in os.environ.get('SERVER_SOFTWARE', ''):
        # Development server
        app.run(host='0.0.0.0', port=port)
    else:
        # Production (Gunicorn will handle it)
        pass
