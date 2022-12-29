import requests

class QuizDB:
    """
    QuizDB is a class that contains all the questions and answers.
    """
    def __init__(self):
        """
        Initialize the QuizDB class.
        """
        response = requests.get("https://englishapi.pythonanywhere.com/api/quiz")
        self.quiz_list = response.json()
    
    def get_quiz(self):
        """
        Return all quiz
        """
        return self.quiz_list

    def get_topic(self, quiz_id):
        """
        Get a specific quiz topics
        """
        url = f"https://englishapi.pythonanywhere.com/api/topic/{quiz_id}"
        response = requests.get(url)
        return response.json()

    def get_question(self, topic_id):
        """
        Get a specific topics questions
        """
        url = f"https://englishapi.pythonanywhere.com/api/question/{topic_id}"
        response = requests.get(url)
        return response.json()

    def get_option(self, question_id):
        """
        Get a specific questions options
        """
        url = f"https://englishapi.pythonanywhere.com/api/option/{question_id}"
        response = requests.get(url)
        return response.json()
