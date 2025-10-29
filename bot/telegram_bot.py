from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers.auth_handler import start_command, button_click, handle_user_input
from config import Config

def create_bot():
    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Core commands and flows
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))

    return app
