from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers.auth_handler import start_command, button_click, handle_user_input
from bot.handlers.hotel_handler import hotel_start, hotel_message_handler
from config import Config

async def main_router(update, context):
    # 🏨 If user is in hotel flow → send to hotel handler
    if context.user_data.get("hotel_flow"):
        return await hotel_message_handler(update, context)

    # 👤 Otherwise handle registration/login flow
    return await handle_user_input(update, context)

def create_bot():
    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Commands & buttons handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click))

    # Hotel command
    app.add_handler(CommandHandler("hotels", hotel_start))

    # Main Message router
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_router))

    return app
