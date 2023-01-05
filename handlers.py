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
url = 'https://englishapi.pythonanywhere.com'
quiz = QuizDB(url)
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
        callback_data = f"topics_{title}_{quiz_id}"
        button = InlineKeyboardButton(
            text=title,
            callback_data=callback_data
        )
        buttons.append([button])
    reply_markup = InlineKeyboardMarkup(buttons)
    query.answer("Waiting!")
    query.edit_message_text("Choose the quiz",reply_markup=reply_markup)
    
def get_topics(update:Update, context:CallbackContext) -> None:
    #Get user id
    user_id = update.callback_query.from_user.id
    #Get callback data
    query = update.callback_query
    data = query.data
    quiz_id = int(data.split('_')[-1])
    quiz_data = quiz.get_topic(quiz_id)

    buttons = []
    for t in quiz_data['quiz']['topics']:
        topic_id = t.get('id')
        title = t.get('title')
        callback_data = f"border_{title}_{quiz_id}"
        button = InlineKeyboardButton(
            text=title,
            callback_data=callback_data
        )
        buttons.append([button])
    reply_markup = InlineKeyboardMarkup(buttons)
    query.answer("Waiting!")
    query.edit_message_text("Choose the topic",reply_markup=reply_markup)

def border(update:Update, context:CallbackContext):
        quer = update.callback_query
        data =quer.data.split('_')
        topic_id = data[-1]
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('5', callback_data=f'questions_{topic_id}_5'), InlineKeyboardButton('10', callback_data=f'questions_{topic_id}_10')],
            [InlineKeyboardButton('15', callback_data=f'questions_{topic_id}_15'), InlineKeyboardButton('20', callback_data=f'questions_{topic_id}_20')],
            [InlineKeyboardButton('25', callback_data=f'questions_{topic_id}_25'), InlineKeyboardButton('30', callback_data=f'questions_{topic_id}_30')],
            [InlineKeyboardButton('40', callback_data=f'questions_{topic_id}_40'), InlineKeyboardButton('50', callback_data=f'questions_{topic_id}_50')]
            ])
        quer.edit_message_text("How many test do you want to solve?", reply_markup=reply_markup)

def question(update:Update, context:CallbackContext) -> None:
    #Get user id
    user_id = update.callback_query.from_user.id
    #Get callback data
    query = update.callback_query
    data = query.data.split('_')
    numpber_of_question = int(data[-1])
    topic_id = int(data[-2])

    print(topic_id, numpber_of_question)
    
