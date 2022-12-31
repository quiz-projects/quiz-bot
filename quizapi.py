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

    def get_option(self, question_id):
        """
        Get a specific questions options
        """
        url = f"{self.base_url}m/api/option/{question_id}"
        response = requests.get(url)
        return response.json()
