from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Replace with your bot's token
BOT_TOKEN='Api Token Bot'
# Replace with your Telegram user ID
YOUR_TELEGRAM_USER_ID = ''

# Dictionary to keep track of users
user_dict = {}

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    user_dict[user.id] = user  # Save the user in the dictionary
    logger.info("User %s started the bot.", user.first_name)
    update.message.reply_text('مرحباً بك في بوت التواصل مع نبيل.')

def echo(update: Update, context: CallbackContext) -> None:
    """Forward received messages to the owner and reply to the user."""
    user = update.effective_user
    try:
        # Forward the message to your personal account
        context.bot.forward_message(
            chat_id=YOUR_TELEGRAM_USER_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        logger.info("Message from user %s forwarded to owner.", user.first_name)

        # Send a confirmation reply to the user
        update.message.reply_text('تم إرسال رسالتك إلى نبيل، وسوف يتم الرد عليك في أقرب وقت ممكن.')
    except Exception as e:
        logger.error("Error forwarding message: %s", str(e))
        update.message.reply_text('عذرًا، حدث خطأ أثناء محاولة إرسال رسالتك. يرجى المحاولة مرة أخرى لاحقًا.')

def reply_to_user(update: Update, context: CallbackContext) -> None:
    """Send a message from the owner to a specific user."""
    if update.effective_user.id != int(YOUR_TELEGRAM_USER_ID):
        update.message.reply_text('عذرًا، هذه الوظيفة مخصصة للمسؤول فقط.')
        return

    try:
        # Message format: /reply user_id Your message here
        args = context.args
        if len(args) < 2:
            update.message.reply_text('يرجى استخدام الصيغة: /reply user_id رسالتك هنا.')
            return

        user_id = int(args[0])
        message_text = ' '.join(args[1:])

        if user_id in user_dict:
            context.bot.send_message(chat_id=user_id, text=message_text)
            update.message.reply_text('تم إرسال رسالتك بنجاح.')
        else:
            update.message.reply_text('المستخدم غير متصل حاليًا أو غير معروف.')

    except Exception as e:
        logger.error("Error sending message to user: %s", str(e))
        update.message.reply_text('حدث خطأ أثناء محاولة إرسال رسالتك.')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the /start command handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Register a handler to echo all received text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Register a command handler for the owner to reply to users
    dispatcher.add_handler(CommandHandler("reply", reply_to_user))

    # Log that the bot has started
    logger.info("Bot started")

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
