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

    def get_question(self, topic_id):
        """
        Get a specific topics questions
        """
        url = f"{self.base_url}/api/question/{topic_id}"
        response = requests.get(url)
        return response.json()

    def add_student(self,user_data):
        
        url = f"{self.base_url}/api/student/"
        response = requests.post(url=url, json=user_data)
        return response.json()

    def update_student(self, question_list, user_id):
        url = f"{self.base_url}/api/updeteStudent/{user_id}"
        response = requests.post(url, json={"question_list":question_list})
        list_data = response.json()['question_list']
        return list_data
    
    def get_student(self, telegram_id):
        url = f"{self.base_url}/api/student/{telegram_id}"
        response = requests.get(url)
        return response.json()

    def add_result(self,data: dict):
        url = f"{self.base_url}/api/result/"
        r = requests.post(url, json=data)
        return r.json()
    
    def get_result(self,student_id, topic_id):
        url = f"{self.base_url}/api/result/{student_id}/{topic_id}"
        r = requests.get(url)
        return r.json()

    def update_result(self, result_id, data:dict):
        url = f'{self.base_url}/api/update_result/{result_id}'
        r = requests.post(url, json=data)
        return r.json()

    def add_result_detail(self, data):
        url = f"{self.base_url}/api/result_detail/"
        r = requests.post(url, json=data)
        return r.json()
    
    def result_detail(self, option_id):
        url = f"{self.base_url}/api/result_detail/{option_id}"
        r = requests.get(url)
        return r.json()
        