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
    border,
    add_option,
    statistics,
    begin_quiz
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
    dp.add_handler(CallbackQueryHandler(add_option, pattern='option'))
    dp.add_handler(CallbackQueryHandler(statistics, pattern='yes'))
    dp.add_handler(CallbackQueryHandler(choose_quiz, pattern='no'))
    dp.add_handler(CallbackQueryHandler(begin_quiz, pattern='chack_member'))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()