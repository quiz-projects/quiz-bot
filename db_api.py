import firebase_admin
from firebase_admin import credentials, firestore

class firestoreDB:
    def __init__(self):
        cred = credentials.Certificate('accountKey.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def set_question(self, telegram_id, data):
        ref = self.db.collection(str(telegram_id)).document('question')
        ref.set(data)
    
    def set_all_percentage(self, telegram_id, data):
        ref = self.db.collection(str(telegram_id)).document('allsolved')
        ref.set(data)

    def get_question(self, telegram_id):
        ref = self.db.collection(str(telegram_id)).document('question')
        questions = ref.get()
        return questions.to_dict()

    def update_question(self, telegram_id, data):
        ref = self.db.collection(str(telegram_id)).document('question')
        ref.update(data)
    
    def add_result(self, telegram_id, data):
        ref = self.db.collection(str(telegram_id)).document('result')
        ref.set({'data':data})

    def get_result(self, telegram_id):
        ref = self.db.collection(str(telegram_id)).document('result')
        return ref.get().to_dict()
    
    def delete_result(self, telegram_id):
        ref = self.db.collection(str(telegram_id)).document('result')
        ref.delete()