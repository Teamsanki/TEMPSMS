import random
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime, timedelta

# Set up logging to view errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global dictionary to store user OTPs and their expiration times
user_otps = {}

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Type "yes" to receive your OTP.')

# Function to handle the "yes" confirmation from the user
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.lower()
    
    # Check if the user confirmed by typing "yes"
    if user_input == "yes":
        otp = generate_otp()
        otp_expiry = datetime.now() + timedelta(minutes=5)  # OTP expires after 5 minutes
        user_otps[update.message.chat_id] = {'otp': otp, 'expiry': otp_expiry}  # Store OTP and expiry time
        update.message.reply_text(f'Your OTP is: {otp}. Please use it within 5 minutes.')
    else:
        update.message.reply_text('Type "yes" to receive your OTP.')

# Function to generate a random OTP
def generate_otp():
    return str(random.randint(1000, 9999))

# Function to validate the OTP
def validate_otp(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_otp = update.message.text.strip()

    # Check if the user has a stored OTP
    if chat_id in user_otps:
        stored_otp = user_otps[chat_id]['otp']
        otp_expiry = user_otps[chat_id]['expiry']
        
        # Check if the OTP is expired
        if datetime.now() > otp_expiry:
            update.message.reply_text("Your OTP has expired. Please type 'yes' again to receive a new one.")
            del user_otps[chat_id]  # Remove expired OTP
        elif user_otp == stored_otp:
            update.message.reply_text("OTP is valid! You've been verified successfully.")
            del user_otps[chat_id]  # Remove OTP after successful validation
        else:
            update.message.reply_text("Invalid OTP. Please try again.")
    else:
        update.message.reply_text("You haven't requested an OTP yet. Type 'yes' to receive one.")

# Error handler function
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    # Replace with your Telegram Bot API Token
    TOKEN = "7700905920:AAG9Encbi28AWUfem_XD3GOtMl_XFXqLKIQ"  # <-- Insert your bot token here!

    # Create the Updater and pass it the bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Handle start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Handle messages from users
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Handle OTP validation (users can type the OTP to validate)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, validate_otp))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a stop signal
    updater.idle()

if __name__ == '__main__':
    main()
