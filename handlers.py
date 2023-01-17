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
    InputMediaPhoto
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
from db_api import firestoreDB
from quizapi import QuizDB
from random import randint
from pprint import pprint
import requests
#Create database object
firestore_db = firestoreDB()
url = 'https://englishapi.pythonanywhere.com'
quiz = QuizDB(url)
chat = "@codeschoolQuiz"
#Start handler
def start(update:Update, context:CallbackContext) -> None:
    #Add user to database
    bot = context.bot
    user = update.message.from_user
    user_id = update.message.chat.id
    data = bot.get_chat_member(chat, user_id)
    status = data["status"]

    #Create user data
    user_data = {
        'first_name': user.first_name, 
        'last_name': user.last_name, 
        'telegram_id': user.id, 
        'username': user.username}
    quiz.add_student(user_data)

    if status == "creator" or status == "member":
        button = InlineKeyboardButton(
            text = "Testni boshlash!", 
            callback_data='start_quiz'
            )
        reply_markup = InlineKeyboardMarkup([[button]])
        # Send message to user
        text ='codeschoolQuizbot ga xush kelibsiz!\n\nTestlarni boshlash uchun quyidagi tugmani bosing!'
        update.message.reply_text(f'{text}',reply_markup=reply_markup)
    else:
        cation =f'codeschoolQuizbot ga xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi guruhga a\'zo bo\'lishingiz kerak! \n👉 {chat}'
        
        button = InlineKeyboardButton(
            text="tekshirish",
            callback_data='chack_member1'
            )
        reply_markup = InlineKeyboardMarkup([[button]])
        update.message.reply_text(cation,reply_markup=reply_markup)

def begin_quiz(update:Update, context:CallbackContext)->None:

    """
    Request permission to start quiz
    """
    user_id = update.callback_query.from_user.id
    #Get callback data
    query = update.callback_query
    bot = context.bot

    query_data = query.data
    data = bot.get_chat_member(chat, user_id)
    status = data["status"]

    if status == "member":
        button = InlineKeyboardButton(
            text = "Testni boshlash!", 
            callback_data='start_quiz'
            )
        reply_markup = InlineKeyboardMarkup([[button]])
        # Send message to user
        query.answer('Weiting!')
        text ='✅ Siz guruhimizga a\'zo bo\'dingiz!\nTestlarni boshlash uchun quyidagi tugmani bosing!'
        query.edit_message_text(f'{text}',reply_markup=reply_markup)

    else:
        # Send message to user
        
        cation1 =f'Siz guruhimizga a\'zo bo\'madingiz, qaytadan urunib ko\'ring!\n👉 {chat}'
        cation2 =f'Guruh username {chat} orqali guruhga a\'zo bo\'ling!'

        if query_data == 'chack_member1':
            button = InlineKeyboardButton(
                text="Tekshirish",
                callback_data='chack_member2'
                )
            reply_markup = InlineKeyboardMarkup([[button]])

            query.edit_message_text(cation1,reply_markup=reply_markup)
        else:
            button = InlineKeyboardButton(
                text=" Qayta tekshirish",
                callback_data='chack_member1'
                )
            reply_markup = InlineKeyboardMarkup([[button]])

            query.edit_message_text(cation2,reply_markup=reply_markup)

def choose_quiz(update:Update, context:CallbackContext) -> None:
    #Get user id
    user_id = update.callback_query.from_user.id
    bot = context.bot
    data = bot.get_chat_member(chat, user_id)
    status = data["status"]
    query = update.callback_query

    #Get callback data
    if status == "creator" or status == "member":
    
        quiz_list = quiz.get_quiz()
        buttons = []
        for q in quiz_list:
            quiz_id = q.get('id')
            title = q.get('title')
            callback_data = f"topics_{quiz_id}"
            button = InlineKeyboardButton(
                text=title,
                callback_data=callback_data
            )
            buttons.append([button])
        reply_markup = InlineKeyboardMarkup(buttons)
        query.answer("Kuting!")
        query.edit_message_text("Test yechish uchun modulni tanlang!",reply_markup=reply_markup)
    else:
        caption=f'Siz guruhimizdan chiqib ketgansiz, Testni davom ettirish uchun guruhga qo\'shiling!\n👉{chat}'
        button = InlineKeyboardButton(
            text="Tekshirish",
            callback_data='chack_member1'
            )
        reply_markup = InlineKeyboardMarkup([[button]])

        query.edit_message_text(caption,reply_markup=reply_markup)

def get_topics(update:Update, context:CallbackContext) -> None:
    #Get user id
    user_id = update.callback_query.from_user.id
    #Get callback data
    query = update.callback_query
    data = query.data
    quiz_id = int(data.split('_')[-1])
    quiz_data = quiz.get_topic(quiz_id)

    buttons = []

    for t in quiz_data['quiz']['topic']:
        topic_id = t.get('id')
        title = t.get('title')
        callback_data = f"border_{topic_id}"
        button = InlineKeyboardButton(
            text=title,
            callback_data=callback_data
        )
        buttons.append([button])
    reply_markup = InlineKeyboardMarkup(buttons)
    query.answer("Kuting!")
    query.edit_message_text("Test yechish uchun mavzu tanlang!",reply_markup=reply_markup)

def border(update:Update, context:CallbackContext):
        quer = update.callback_query
        data =quer.data.split('_')
        topic_id = data[-1]
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('5', callback_data=f'questions_{topic_id}_5'), InlineKeyboardButton('10', callback_data=f'questions_{topic_id}_10')],
            [InlineKeyboardButton('15', callback_data=f'questions_{topic_id}_15'), InlineKeyboardButton('20', callback_data=f'questions_{topic_id}_20')]])
        quer.edit_message_text("Nechta test yechishni hohlaysiz?", reply_markup=reply_markup)


def keyboard(options, result_id, question_id):

    buttons = []
    for option in options:
        title = option['title']
        is_correct = option['is_correct']
        option_id = option['id']
        button = InlineKeyboardButton(
            title, 
            callback_data=f'nextquestion_{title}_{is_correct}_{option_id}_{result_id}_{question_id}')
        buttons.append(button)

    return buttons

def question(update:Update, context:CallbackContext) -> None:
    query = update.callback_query
    #Get user id
    telegram_id = query.from_user.id
    bot = context.bot
    data = query.data.split('_')
    question_numpber = int(data[-1])
    topic_id = int(data[-2])

    question = quiz.get_question(topic_id,telegram_id,question_numpber)

    questions = question['quiz']['topic']['question']
    result_id = question['quiz']['result']
    question = questions.pop()
    firestore_db.set_question(telegram_id, data={'questions':questions})
    firestore_db.add_result(telegram_id,[])
    
    question_id = question['id']
    options = question['option']
    image = question['img']
    title = question['title']

    reply_markup = InlineKeyboardMarkup([keyboard(options, result_id, question_id)])

    firestore_db.update_question(telegram_id, {'questions':questions})
    query.edit_message_text("Savollarni yechishni boshlang!")
    bot.sendPhoto(chat_id=telegram_id ,photo=image, caption=title, reply_markup = reply_markup)


def next_question(update:Update, context:CallbackContext) -> None:
    query = update.callback_query
    #Get user id
    telegram_id = query.from_user.id
    bot = context.bot

    data = query.data.split('_')

    text_handler,title, is_correct, option_id, result_id, question_id = data

    result = {
        "result":result_id, 
        "question":question_id, 
        "option":option_id,
        "is_correct":is_correct == "True"
    }

    results:list = firestore_db.get_result(telegram_id)['data']
    results.append(result)
    firestore_db.add_result(telegram_id, results)

    questions = firestore_db.get_question(telegram_id)['questions']
    if len(questions) > 0:
        question = questions.pop()
        firestore_db.update_question(telegram_id, {'questions':questions})

        question_id = question['id']
        options = question['option']
        image = question['img']
        title = question['title']
        reply_markup = InlineKeyboardMarkup([keyboard(options, result_id, question_id)])

        if is_correct == 'True':
            query.edit_message_caption("To'g'ri javob berdingiz ✅")
        else:
            query.edit_message_caption("Noto'g'ri javob berdingiz ❌")
        bot.sendPhoto(chat_id=telegram_id ,photo=image, caption=title, reply_markup = reply_markup)

    else:
        if is_correct == 'True':
            query.edit_message_caption("To'g'ri javob berdingiz ✅")
        else:
            query.edit_message_caption("Noto'g'ri javob berdingiz ❌")

        results:list = firestore_db.get_result(telegram_id)['data']
        correct = 0
        for result in results:
            correct += result['is_correct']

        quiz.add_result_detail(results)
        firestore_db.delete_result(telegram_id)

        text = f"Umumiy savollar soni: {len(results)}\nTo'g'ri javoblar soni: {correct}"
        bot.sendMessage(telegram_id,text)