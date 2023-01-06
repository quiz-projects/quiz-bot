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
from quizapi import QuizDB
from random import randint
from pprint import pprint
import requests
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
        'first_name': user.first_name, 
        'last_name': user.last_name, 
        'telegram_id': user.id, 
        'username': user.username, 
        "question_list":[]}
    quiz.add_student(user_data)

    button = InlineKeyboardButton(
        text = "Testni boshlash!", 
        callback_data='start_quiz'
        )
    reply_markup = InlineKeyboardMarkup([[button]])
    # Send message to user
    text ='codeschoolQuizbot ga xush kelibsiz!\n\nTestlarni boshlash uchun quyidagi tugmani bosing!'
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
    query.answer("Kuting!")
    query.edit_message_text("Test yechish uchun modulni tanlang!",reply_markup=reply_markup)
    
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
        callback_data = f"border_{title}_{topic_id}"
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

def question(update:Update, context:CallbackContext) -> None:
    #Get user id
    telegram_id = update.callback_query.from_user.id
    bot = context.bot
    #Get callback data
    query = update.callback_query
    data = query.data.split('_')
    numpber_of_question = int(data[-1])
    quiz.current_question = numpber_of_question
    topic_id = int(data[-2])
    
    random_list = []
    user_id = quiz.get_student(telegram_id)['id']
    
    data = {"student": user_id, "topic": topic_id, "score": 0}
    result_data = quiz.add_result(data)
    result_id = result_data['id']
    question = quiz.get_question(topic_id)

    quiz.update_result(result_id, {"current_question_number":numpber_of_question})

    questions = question['quiz']['topic']["question"]
    idx = list(range(len(questions)))
    for i in range(numpber_of_question):
        
        random_list.append(randint(idx[0],idx[-1]))

    question_list = quiz.update_student(random_list, user_id)
    
    if len(question_list) > 0:
        img = question['quiz']['topic']['question'][random_list[0]]["img"]

        keyboard = [[]]
        for option in question['quiz']['topic']['question'][random_list[0]]["option"]:
                question_id = option["question"]
                option_id = option['id']
                button = InlineKeyboardButton(
                    option["title"], 
                    callback_data=f"option_{question_id}_{option_id}_{result_id}_{topic_id}")
                keyboard[0].append(button)
                
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = question['quiz']['topic']['question'][question_list[0]]["title"]
        query.edit_message_text("Savollarni yechishni boshlang!")
        bot.sendPhoto(telegram_id ,img, text, reply_markup = reply_markup)

        if len(question_list) > 0:
            question_list.pop(0)
            quiz.update_student(question_list, user_id)
    else:
        b1 = InlineKeyboardButton('Yes', callback_data=f'yes_{topic_id}_{user_id}_{result_id}')
        b2 = InlineKeyboardButton("No", callback_data='no')
        reply_markup = InlineKeyboardMarkup([[b1, b2]])
        bot.sendMessage(telegram_id,'Bu mavzuni muvaffaqiyatli tugatdingiz.\n✅Natijarni ko\'rishni hohlaysizmi?',reply_markup=reply_markup)

def next_question(update:Update, context:CallbackContext, topic_id:int, result_id:int, chat_id:int) -> None:
    telegram_id = update.callback_query.from_user.id
    bot = context.bot

    user_data = quiz.get_student(chat_id)
    user_id = user_data['id']
    questions = user_data["question_list"]
    question = quiz.get_question(topic_id)
    if len(questions) > 0:
        img = question['quiz']['topic']['question'][questions[0]]["img"]

        keyboard = [[]]
        for option in question['quiz']['topic']['question'][questions[0]]["option"]:
                question_id = option["question"]
                option_id = option['id']
                button = InlineKeyboardButton(
                    option["title"], 
                    callback_data=f"option_{question_id}_{option_id}_{result_id}_{topic_id}")
                keyboard[0].append(button)
                
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = question['quiz']['topic']['question'][questions[0]]["title"]
        bot.sendPhoto(chat_id ,img, text, reply_markup = reply_markup)

        if len(questions) > 0:
            questions.pop(0)
            quiz.update_student(questions, user_data['id'])
        
    else:
        b1 = InlineKeyboardButton('Ha', callback_data=f'yes_{topic_id}_{user_id}_{result_id}')
        b2 = InlineKeyboardButton("Yoq", callback_data='no')
        reply_markup = InlineKeyboardMarkup([[b1, b2]])
        bot.sendMessage(telegram_id,'Bu mavzuni muvaffaqiyatli tugatdingiz✅\nNatijarni ko\'rishni hohlaysizmi?',reply_markup=reply_markup)

def add_option(update:Update, context:CallbackContext) -> None:
    query = update.callback_query 
    data = query.data.split('_')  
    question_id = int(data[1])
    option_id = int(data[2])
    result_id = int(data[3])
    topic_id = int(data[4])
    student_id = int(quiz.get_student(query.message.chat.id)['id'])
    data_json = {
        "result":result_id, 
        "question":question_id, 
        "option":option_id
    }
    result_data = quiz.add_result_detail(data_json)

    result_option = quiz.result_detail(option_id)

    if result_option["is_correct"] == False:
        query.answer("Noto'g'ri javob berdingiz ❌")
        query.edit_message_caption('Noto\'g\'ri javob berdingiz ❌', reply_markup=None)

    if result_option["is_correct"] == True:
        get_result_data = quiz.get_result(student_id, topic_id)
        current_question_result = int(get_result_data['student']["results"][0]["current_question_result"]) + 1
        quiz.update_result(result_id, {"current_question_result":current_question_result})
        query.answer("To'g'ri javob berdingiz ✅")
        query.edit_message_caption('To\'g\'ri javob berdingiz ✅', reply_markup=None)
    next_question(update, context, topic_id, result_id, query.message.chat.id)

def statistics(update:Update, context:CallbackContext):
    query = update.callback_query
    data = query.data.split('_')
    student_id = data[-2]
    topic_id = data[-3]
    result_id = data[-1]
    student_result = quiz.get_result(student_id, topic_id)

    now_answer = student_result["student"]["results"][0]["current_question_result"]
    current_question = student_result["student"]["results"][0]["current_question_number"]

    text = f"Umumiy savollar soni: {current_question}\nTo'g'ri javoblar soni: {now_answer}\nMavzu bo'yicha umimiy to'g'ri javoblar soni: " + str(student_result['student']["results"][0]["score"])
    query.edit_message_text(text, reply_markup=None)
    quiz.update_result(result_id, {
        "current_question_number":0,
        "current_question_result":0
        })


