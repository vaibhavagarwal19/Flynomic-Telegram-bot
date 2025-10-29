from bot.telegram_bot import create_bot

if __name__ == "__main__":
    app = create_bot()
    print("🚀 Flynomic Telegram Bot is running...")
    app.run_polling()
