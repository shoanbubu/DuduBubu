import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import Forbidden

# ✅ Correct token assignment (Use environment variable OR direct assignment)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Preferred: Set this in your environment variables
# TOKEN = "YOUR_BOT_TOKEN"  # Hardcoded (Use only for testing)

CHANNEL_ID = "@Btec2025"  # Updated group/channel name

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

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        photo = update.message.photo[-1].file_id
        caption = update.message.caption if update.message.caption else "Anonymous Photo"
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=caption)
    except Exception as e:
        await update.message.reply_text("❌ Failed to send the photo. Please try again.")
        print(f"Error sending photo: {e}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        video = update.message.video.file_id
        caption = update.message.caption if update.message.caption else "Anonymous Video"
        await context.bot.send_video(chat_id=CHANNEL_ID, video=video, caption=caption)
    except Exception as e:
        await update.message.reply_text("❌ Failed to send the video. Please try again.")
        print(f"Error sending video: {e}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        document = update.message.document.file_id
        caption = update.message.caption if update.message.caption else "Anonymous Document"
        await context.bot.send_document(chat_id=CHANNEL_ID, document=document, caption=caption)
    except Exception as e:
        await update.message.reply_text("❌ Failed to send the document. Please try again.")
        print(f"Error sending document: {e}")

def main() -> None:
    if not TOKEN:
        print("❌ Error: Bot token is missing! Set TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_document))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
