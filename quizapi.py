import requests

class QuizDB:
    """
    QuizDB is a class that contains all the questions and answers.
    """
    def __init__(self, base_url):
        """
        Initialize the QuizDB class.
        """
        self.base_url = base_url
    
    def get_quiz(self):
        """
        Return all quiz
        """
        response = requests.get(f"{self.base_url}/api/quiz")
        quiz_list = response.json()
        return quiz_list

    def get_topic(self, quiz_id):
        """
        Get a specific quiz topics
        """
        url = f"{self.base_url}/api/topic/{quiz_id}"
        response = requests.get(url)
        return response.json()

    def get_question(self, topic_id,telegram_id,question_number):
        """
        Get a specific topics questions
        """
        url = f"{self.base_url}/api/question/{topic_id}/{question_number}?telegram_id={telegram_id}"
        response = requests.get(url)
        return response.json()

    def add_student(self,user_data):
        
        url = f"{self.base_url}/api/student/"
        response = requests.post(url=url, json=user_data)
        return response.json()
    
    def get_student(self, telegram_id):
        url = f"{self.base_url}/api/student/{telegram_id}"
        response = requests.get(url)
        return response.json()

    def add_result_detail(self, data:list):
        url = f"{self.base_url}/api/result_detail/"
        requests.post(url, json=data)

    def allPercentage(self, telegram_id, quiz_id):
        url = f"{self.base_url}/api/get_all_percentage/{telegram_id}/{quiz_id}"
        responce = requests.get(url)
        return responce.json()
    
    def get_percentage(self, telegram_id, topic_id):
        url = f"{self.base_url}/api/get_percentage/{telegram_id}/{topic_id}"
        responce = requests.get(url)
        return responce.json()