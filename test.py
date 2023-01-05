import requests
from quizapi import QuizDB
from pprint import pprint

url = 'https://englishapi.pythonanywhere.com'
quiz = QuizDB(url)

pprint(quiz.get_topic(1))
