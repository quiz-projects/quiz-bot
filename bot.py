from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
    
)
from handlers import (
    start,
    choose_quiz,
    get_topics,
    question,
    border
)
import os
TOKEN = os.environ['TOKEN']

def main() -> None:
    """
    Run the bot.
    """
    # Create the Updater and pass it your bot's token.

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(choose_quiz, pattern='start_quiz'))
    dp.add_handler(CallbackQueryHandler(get_topics, pattern='topics'))
    dp.add_handler(CallbackQueryHandler(border, pattern='border'))
    dp.add_handler(CallbackQueryHandler(question, pattern='questions'))
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()