from bot.telegram_bot import create_bot
from telegram import Update

if __name__ == "__main__":
    app = create_bot()
    print("🚀 Flynomic Telegram Bot is running...")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

