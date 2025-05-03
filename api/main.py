from typing import Union
from fastapi import FastAPI

import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate('re2ake-2d4df28a7960.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "See you on Re2ake!"}

# the public API
@app.get("/ask")
def ask_question(q: str):
    # query the OpenAI API if it found something in the existing FAQ, or we should forward this to the operator
    
    # forwarding means adding a new entry in the 'questions' collection in the DB

    return {'answer': 'kys'}

# the private operator/admin API (no auth yet)
@app.get("/faq")
def get_faq():
    faqs = db.collection('faq').get()
    for faq in faqs:
        print(faq.id, '=>', faq.to_dict())
    return {}

@app.put("/faq")
def add_faq(q: str, a: str):
    time, ref = db.collection('faq').add({
        'q': q,
        'a': a
    })
    return {'faq_id': ref.id}

@app.delete("/faq/{faq_id}")
def delete_faq(faq_id: str):
    db.collection('faq').document(faq_id).delete()
    return {}

@app.get("/questions")
def get_questions():
    qs = db.collection('questions').get()
    questions = []
    for q in qs:
        print(q.id, '=>', q.to_dict())
        questions.append(q.to_dict())
    return questions

@app.get("/questions/{qid}")
def get_question(qid: int):
    return {}

@app.delete("/questions/{qid}")
def delete_question(qid: int):
    db.collection('questions').document(qid).delete()
    return {}
