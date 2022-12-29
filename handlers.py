from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    Dispatcher
)
from quizapi import QuizDB
#Create database object
quiz = QuizDB()
#Start handler
def start(update:Update, context:CallbackContext) -> None:
    #Add user to database
    user = update.message.from_user
    user_id = update.message.from_user.id
    #Create user data
   
    user_data = {
        'user_id': user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
    }
    button = InlineKeyboardButton(
        text = "Start Quiz!", 
        callback_data='start_quiz'
        )
    reply_markup = InlineKeyboardMarkup([[button]])
    # Send message to user
    text ='Welcome to Quiz Bot!\n\nClick the button below to take the quiz!'
    update.message.reply_text(f'{text}',reply_markup=reply_markup)

def choose_quiz(update:Update, context:CallbackContext) -> None:
    #Get user id
    user_id = update.callback_query.from_user.id
    #Get callback data
    query = update.callback_query
    # Get all quiz
    quiz_list = quiz.get_quiz()
    buttons = []
    for q in quiz_list:
        quiz_id = q.get('id')
        title = q.get('title')
        callback_data = f"{title}_{quiz_id}"
        button = InlineKeyboardButton(
            text=title,
            callback_data=callback_data
        )
        buttons.append(button)
    reply_markup = InlineKeyboardMarkup([buttons])
    query.answer("Waiting!")
    query.edit_message_text("Choose the quiz",reply_markup=reply_markup)
    
