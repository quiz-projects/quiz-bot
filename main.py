from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
    Dispatcher
    
)
from handlers import (
    start,
    choose_quiz,
    get_topics,
    question,
    next_question,
    border,
    begin_quiz
)

import os
import telegram
import functions_framework

TOKEN = os.environ.get('TOKEN')
# Create bot instance
bot = telegram.Bot(token=TOKEN)

@functions_framework.http
def main(request):
   # Check if request is POST
   if request.method == 'POST':
        # Create a dispatcher instance
        dp = Dispatcher(bot, None,workers=0)
        # Get update from request
        update = Update.de_json(request.get_json(force=True), bot)
        # Add handlers
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CallbackQueryHandler(choose_quiz, pattern='start_quiz'))
        dp.add_handler(CallbackQueryHandler(get_topics, pattern='topics'))
        dp.add_handler(CallbackQueryHandler(border, pattern='border'))
        dp.add_handler(CallbackQueryHandler(question, pattern='questions'))
        dp.add_handler(CallbackQueryHandler(next_question, pattern='nextquestion'))
        dp.add_handler(CallbackQueryHandler(begin_quiz, pattern='chack_member'))

        dp.process_update(update) 
        return {'ok':TOKEN}
   
   return f'TOKEN: {TOKEN}!'