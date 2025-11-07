from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ContextTypes
from services.hotel_service import search_hotels
from datetime import datetime
import logging
import requests

logger = logging.getLogger(__name__)

async def hotel_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["hotel_flow"] = "get_place"
    await update.message.reply_text("🏨 Enter destination (e.g., Dubai, UAE):")


async def hotel_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("hotel_flow")
    user_id = update.effective_user.id

    if state == "get_place":
        context.user_data["place"] = update.message.text
        context.user_data["hotel_flow"] = "checkin"
        await update.message.reply_text("📅 Enter Check-in date (YYYY-MM-DD):")
        return

    elif state == "checkin":
        try:
            checkin_date = datetime.strptime(update.message.text, "%Y-%m-%d").date()
            if checkin_date <= datetime.now().date():
                await update.message.reply_text("❌ Date must be in the future.")
                return
        except ValueError:
            await update.message.reply_text("⚠️ Invalid format. Use YYYY-MM-DD.")
            return

        context.user_data["checkin"] = update.message.text
        context.user_data["hotel_flow"] = "checkout"
        await update.message.reply_text("📅 Enter Check-out date (YYYY-MM-DD):")
        return

    elif state == "checkout":
        context.user_data["checkout"] = update.message.text

        # ✅ Prepare data for webview
        place = context.user_data["place"]
        checkin = context.user_data["checkin"]
        checkout = context.user_data["checkout"]

        # ✅ Secure HTTPS URL required by Telegram
        web_url = (
            f"https://flynomic.com/hotels-list?"
            f"user_id={user_id}&place={place}&checkin={checkin}&checkout={checkout}"
        )

        keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("View Hotels 🌐", web_app=WebAppInfo(url=web_url))]],
            resize_keyboard=True
        )

        await update.message.reply_text(
            "👇 Tap below to view available hotels in webview",
            reply_markup=keyboard
        )

        context.user_data["hotel_flow"] = None
        logger.info(f"Hotel flow complete for user {user_id}")
