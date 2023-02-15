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
import check_topics
import requests
#Create database object
firestore_db = firestoreDB()
url = 'https://englishapi.pythonanywhere.com'
quiz = QuizDB(url)
chat = "@codeschoolQuiz"
#Start handler
def start(update:Update, context:CallbackContext) -> None:
    """
    Start the bot and add user to database
    """
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
        text ="CODESCHOOL quiz botga xush kelibsiz!\n\nDasturlash bo'yicha bilimingizni biz bilan oshiring!"
        update.message.reply_text(f'{text}',reply_markup=reply_markup)
    else:
        cation =f'CODESCHOOL quiz botga xush kelibsiz!\n\nBotdan foydalanish uchun quyidagi guruhga a\'zo bo\'lishingiz kerak! \n👉 {chat}'
        
        button = InlineKeyboardButton(
            text="Tekshirish",
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

    # Get user status from telegram group
    data = bot.get_chat_member(chat, user_id)
    status = data["status"]
    # check user status form telegram group
    if status == "member":
        button = InlineKeyboardButton(
            text = "Testni boshlash!", 
            callback_data='start_quiz'
            )
        reply_markup = InlineKeyboardMarkup([[button]])
        # Send message to user
        query.answer('Kuting...')
        text ='✅ Siz guruhimizga a\'zo bo\'dingiz!\nTestlarni boshlash uchun quyidagi tugmani bosing!'
        query.edit_message_text(f'{text}',reply_markup=reply_markup)

    else:
        # Send message to user
        caption1 =f'Siz guruhimizga a\'zo bo\'madingiz, qaytadan urunib ko\'ring!\n👉 {chat}'
        caption2 =f'Guruh username {chat} orqali guruhga a\'zo bo\'ling!'

        if query_data == 'chack_member1':
            button = InlineKeyboardButton(
                text="Tekshirish",
                callback_data='chack_member2'
                )
            reply_markup = InlineKeyboardMarkup([[button]])

            query.edit_message_text(caption1,reply_markup=reply_markup)
        else:
            button = InlineKeyboardButton(
                text=" Qayta tekshirish",
                callback_data='chack_member1'
                )
            reply_markup = InlineKeyboardMarkup([[button]])

            query.edit_message_text(caption2,reply_markup=reply_markup)

def choose_quiz(update:Update, context:CallbackContext) -> None:
    """
    Choose quiz from list
    """
    #Get user id
    user_id = update.callback_query.from_user.id
    bot = context.bot
    # Get user status from telegram group
    data = bot.get_chat_member(chat, user_id)
    status = data["status"]
    query = update.callback_query
    # check user status form telegram group
    if status == "creator" or status == "member":
        # Get quiz list from database
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
        query.answer("Kuting...")
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
    telegram_id = query.from_user.id
    data = query.data
    quiz_id = int(data.split('_')[-1])
    quiz_data = quiz.get_topic(quiz_id)
    allsolved = quiz.allPercentage(telegram_id, quiz_id)
    buttons = []

    min_topic_id = check_topics.fist_topic_id(quiz_data)
    for t in quiz_data['quiz']['topic']:
        topic_id = t.get('id')
        title = t.get('title')
        score = allsolved['allsolved'].get(title, 0)
        
        if allsolved['allsolved'].get(title, 0) >=70 or topic_id == min_topic_id:
            key = f"✅ {score}%"
            title = title + key
        else:
            key = f"🔒 {score}%"
            title = title + key

        callback_data = f"border_{min_topic_id}_{topic_id}_{quiz_id}_{key}"
        button = InlineKeyboardButton(
            text=title,
            callback_data=callback_data
        )
        buttons.append([button])
    buttons.append([InlineKeyboardButton("Modul tanlash", callback_data="start_quiz")])
    reply_markup = InlineKeyboardMarkup(buttons)
    query.answer("Kuting!")
    query.edit_message_text("Test yechish uchun mavzu tanlang!",reply_markup=reply_markup)
    firestore_db.set_all_percentage(telegram_id, allsolved)

def border(update:Update, context:CallbackContext):
    """
    Choose number of questions from question list
    """

    telegram_id = update.callback_query.from_user.id
    quer = update.callback_query
    # get callback data
    data =quer.data.split('_')
    min_topic_id = data[-4]
    topic_id = data[-3]
    quiz_id = data[-2]
    key = data[-1]
    check_topic = check_topics.check_above_topics(quiz,telegram_id, topic_id, min_topic_id)
    if check_topic:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('5', callback_data=f'questions_{quiz_id}_{topic_id}_5'), InlineKeyboardButton('10', callback_data=f'questions_{quiz_id}_{topic_id}_10')],
            [InlineKeyboardButton('15', callback_data=f'questions_{quiz_id}_{topic_id}_15'), InlineKeyboardButton('20', callback_data=f'questions_{quiz_id}_{topic_id}_20')],
            [InlineKeyboardButton("Mavzu tanlash", callback_data=f"topics_{quiz_id}")]])
        quer.edit_message_text("Nechta test yechishni hohlaysiz?", reply_markup=reply_markup)
    else:
        quer.answer("🔒 Bu mavzuni yechish uchun yuqoridagi mavzuda o'zlashtirish darajangiz 70%dan yuqori bo'lishi kerak!", show_alert=True)

def keyboard(options, result_id, question_id, topic_id, quiz_id):
    """
    Create keyboard for question

    Args:
        options (list): List of options
        result_id (int): Result id
        question_id (int): Question id
        quiz_id (int): Quiz id
    Returns:
        list: List of buttons
    """
    buttons = []
    for option in options:
        title = option['title']
        is_correct = option['is_correct']
        option_id = option['id']
        button = InlineKeyboardButton(
            title, 
            callback_data=f'nextquestion_{quiz_id}_{topic_id}_{title}_{is_correct}_{option_id}_{result_id}_{question_id}')
        buttons.append(button)

    return buttons

def question(update:Update, context:CallbackContext) -> None:
    """
    Start question and send first question
    """
    query = update.callback_query
    #Get user id
    telegram_id = query.from_user.id
    bot = context.bot
    # get callback data
    data = query.data.split('_')
    question_numpber = int(data[-1])
    topic_id = int(data[-2])
    quiz_id = int(data[-3])
    # Get question from database
    question = quiz.get_question(topic_id,telegram_id,question_numpber)

    questions = question['quiz']['topic']['question']
    result_id = question['quiz']['result']
    question = questions.pop()
    # Keep a set of question to temporary database
    firestore_db.set_question(telegram_id, data={'questions':questions})
    # Add result to temporary database
    firestore_db.add_result(telegram_id,[])
    
    question_id = question['id']
    options = question['option']
    image = question['img']
    title = question['title']

    reply_markup = InlineKeyboardMarkup([keyboard(options, result_id, question_id,topic_id, quiz_id)])
    # Update question to temporary database
    firestore_db.update_question(telegram_id, {'questions':questions})
    query.edit_message_text("Savollarni yechishni boshlang!")
    # send first question
    bot.sendPhoto(chat_id=telegram_id ,photo=image, caption=title, reply_markup = reply_markup)

def isCorrect(query, is_correct):
    """
    Check answer is correct or not

    Args:
        query (Update): query data
        is_correct (str): True or False
    Returns:
        None
    """
    if is_correct == 'True':
        query.edit_message_caption("To'g'ri javob berdingiz ✅")
    else:
        query.edit_message_caption("Noto'g'ri javob berdingiz ❌")
    
def next_question(update:Update, context:CallbackContext) -> None:
    """
    Send next question
    """
    query = update.callback_query
    #Get user id
    telegram_id = query.from_user.id
    bot = context.bot

    data = query.data.split('_')

    text_handler, quiz_id, topic_id, title, is_correct, option_id, result_id, question_id = data

    result = {
        "result":result_id, 
        "question":question_id, 
        "option":option_id,
        "is_correct":is_correct == "True"
    }
    # Get result from temporary database
    results:list = firestore_db.get_result(telegram_id)['data']
    # Add result to temporary database one by one
    results.append(result)
    # Update result to temporary database
    firestore_db.add_result(telegram_id, results)
    # Get question from temporary database
    questions = firestore_db.get_question(telegram_id)['questions']
    if len(questions) > 0:
        # Get question from temporary database and remove it
        question = questions.pop()
        # Update question to temporary database
        firestore_db.update_question(telegram_id, {'questions':questions})

        question_id = question['id']
        options = question['option']
        image = question['img']
        title = question['title']
        reply_markup = InlineKeyboardMarkup([keyboard(options, result_id, question_id,topic_id, quiz_id)])
        # Send edit message caption
        isCorrect(query, is_correct)
        # Send next question
        bot.sendPhoto(chat_id=telegram_id ,photo=image, caption=title, reply_markup = reply_markup)

    else:
        # Send edit message caption
        isCorrect(query, is_correct)
        # Get result from temporary database
        results:list = firestore_db.get_result(telegram_id)['data']
        # Get result detail from database
        correct = 0
        for result in results:
            correct += result['is_correct']

        button1  = InlineKeyboardButton("Modul tanlash", callback_data="start_quiz")
        button2  = InlineKeyboardButton("Mavzu tanlash", callback_data=f"topics_{quiz_id}")
        reply_markup = InlineKeyboardMarkup([[button1, button2]])
        quiz.add_result_detail(results)
        topic_persentage = quiz.get_percentage(telegram_id, topic_id)['solved']
        if topic_persentage >= 70:
            condition = "✅"
        else:
            # lock emoji
            condition = "🔒"
        text = f"Umumiy savollar soni: {len(results)}\nTo'g'ri javoblar soni: {correct}\n\n{condition} Ushbu mavzuni o'zlashtirish darajangiz: {topic_persentage}%"
        # Send result
        bot.sendMessage(telegram_id,text, reply_markup=reply_markup)
        # Add result detail to database
        # quiz.add_result_detail(results)
        # Delete result from temporary database 
        firestore_db.delete_result(telegram_id)