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
    return {}

@app.delete("/faq/{faq_id}")
def delete_faq(faq_id: int):
    return {}

@app.get("/questions")
def get_questions():
    return {}

@app.get("/questions/{qid}")
def get_question(qid: int):
    return {}
