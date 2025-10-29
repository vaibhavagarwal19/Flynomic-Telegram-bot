from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import register_user, resend_otp, verify_otp
from config import Config

# Step 1: /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Register", callback_data="register")],
        [InlineKeyboardButton("🔐 Login", callback_data="login")],
        [
            InlineKeyboardButton("🌐 Visit Website", url=Config.WEBSITE_URL),
            InlineKeyboardButton("ℹ️ Learn More", callback_data="learn_more")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 *Welcome to Flynomic Bot!* ✈️\n\nChoose an option below:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# Step 2: Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "register":
        context.user_data["flow"] = "register_first_name"
        await query.edit_message_text("Please enter your *First Name*:", parse_mode="Markdown")

    elif query.data == "login":
        context.user_data["flow"] = "login_email"
        await query.edit_message_text("Please enter your *Email* to login:", parse_mode="Markdown")

    elif query.data == "learn_more":
        await query.edit_message_text(
            "✈️ *Flynomic* helps you search and book flights & hotels directly within Telegram.",
            parse_mode="Markdown"
        )


# Step 3: Handle user input text messages
async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flow = context.user_data.get("flow")

    # =============== Registration Flow ===============
    if flow == "register_first_name":
        context.user_data["first_name"] = update.message.text
        context.user_data["flow"] = "register_last_name"
        await update.message.reply_text("Enter your *Last Name*:", parse_mode="Markdown")

    elif flow == "register_last_name":
        context.user_data["last_name"] = update.message.text
        context.user_data["flow"] = "register_email"
        await update.message.reply_text("Enter your *Email Address*:")

    elif flow == "register_email":
        context.user_data["email"] = update.message.text
        context.user_data["flow"] = "register_phone"
        await update.message.reply_text(
            "Enter your *Phone Number* (or type 'skip' to continue):", parse_mode="Markdown"
        )

    elif flow == "register_phone":
        first = context.user_data["first_name"]
        last = context.user_data["last_name"]
        email = context.user_data["email"]
        phone = update.message.text if update.message.text.lower() != "skip" else ""

        context.user_data["phone"] = phone
        response = register_user(first, last, email, phone)

        if "error" in response:
            await update.message.reply_text("❌ Registration failed. Please try again later.")
        else:
            context.user_data["flow"] = "otp_verify"
            context.user_data["mode"] = "register"
            await update.message.reply_text("✅ Registered successfully! Please enter the OTP sent to your email.")

    # =============== OTP Verification (Common) ===============
    elif flow == "otp_verify":
        otp = update.message.text
        email = context.user_data["email"]
        response = verify_otp(email, otp)

        if "error" in response:
            await update.message.reply_text("❌ Invalid or expired OTP. Please try again.")
        else:
            first_name = context.user_data.get("first_name", "Traveler")
            context.user_data.clear()
            await update.message.reply_text(f"🎉 Welcome, *{first_name}!* You're successfully logged in to *Flynomic* ✈️", parse_mode="Markdown")

    # =============== Login Flow ===============
    elif flow == "login_email":
        context.user_data["email"] = update.message.text
        context.user_data["flow"] = "login_phone"
        await update.message.reply_text(
            "Enter your *Phone Number* (or type 'skip' to continue):", parse_mode="Markdown"
        )

    elif flow == "login_phone":
        email = context.user_data["email"]
        phone = update.message.text if update.message.text.lower() != "skip" else ""

        context.user_data["phone"] = phone
        response = resend_otp("", "", email, phone)

        if "error" in response:
            await update.message.reply_text("❌ Login failed. Please check your email.")
        else:
            context.user_data["flow"] = "otp_verify"
            context.user_data["mode"] = "login"
            await update.message.reply_text("📩 OTP sent! Please enter the OTP sent to your email.")
