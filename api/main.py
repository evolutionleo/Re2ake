from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from ai.ai import Answerer

import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.Certificate('re2ake-2d4df28a7960.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

ai = Answerer()


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "See you on Re2ake!"}

# the public API
@app.get("/ask")
def ask_question(q: str, user_id: int, message_id: int):
    # query the OpenAI API if it found something in the existing FAQ, or we should forward this to the operator
    # answer, isSuccess = ai.answer(q, get_faqs())
    answer, isSuccess = 'kys', False

    if not isSuccess:
        # if we don't have an answer from the AI, we should forward the question to the operator
        # add a new entry in the 'questions' collection in the DB
        db.collection('questions').add({
            'q': q,
            'user_id': user_id,
            'message_id': message_id,
            'status': 'unanswered'
        })
    else:
        db.collection('questions').add({
            'q': q,
            'user_id': user_id,
            'message_id': message_id,
            'status': 'autoanswered',
            'answer': answer
        })

    # forwarding means adding a new entry in the 'questions' collection in the DB
    return {'answer': answer, 'isSuccess': isSuccess}


# methods used by the bot to get the answers from the operator and send them to the user
# there is no separate collection for the manual answers, they're just stored with the questions,
# but marked with status='answered' (as opposed to 'unanswered', 'autoanswered' or 'sent')
@app.get("/answers")
def get_answers():
    answers = [{ 'a': a.to_dict(), 'id': a.id } for a in db.collection('questions').where(filter=FieldFilter('status', '==', 'answered')).get()]
    return answers

@app.delete("/answers/{qid}")
def get_answers(qid: str):
    db.collection('questions').document(qid).set({
        'status': 'sent'
    })
    return {}


# the private operator/admin API (no auth yet)
@app.get("/faq")
def get_faqs():
    faqs = [faq.to_dict() for faq in db.collection('faq').get()]
    return faqs

@app.post("/faq")
def add_faq(q: str, a: str):
    time, ref = db.collection('faq').add({
        'q': q,
        'a': a
    })
    return {'faq_id': ref.id}

@app.get("/faq/{faq_id}")
def get_faq(faq_id: str):
    faq = db.collection('faq').document(faq_id).get().to_dict()
    return faq

@app.delete("/faq/{faq_id}")
def delete_faq(faq_id: str):
    db.collection('faq').document(faq_id).delete()
    return {}

@app.get("/questions/all")
def get_all_questions():
    questions = [q.to_dict() for q in db.collection('questions').get()]
    return questions

@app.get("/questions/unanswered")
def get_pending_questions():
    questions = [q.to_dict() for q in db.collection('questions').where(filter=FieldFilter('status', '==', 'unanswered')).get()]
    return questions

@app.get("/questions/{qid}")
def get_question(qid: str):
    q = db.collection('questions').document(qid).get().to_dict()
    return {'q': q}

@app.delete("/questions/{qid}")
def delete_question(qid: str):
    db.collection('questions').document(qid).delete()
    return {}

@app.post("/answer/{qid}")
def answer_question(qid: str, a: str):
    db.collection('questions').document(qid).set({
        'status': 'answered',
        'answer': a
    })
    return {}