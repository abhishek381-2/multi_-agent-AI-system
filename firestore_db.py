import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# --- Firestore Initialization ---
# serviceAccountKey.json file ka istemaal karein
# credentials.Certificate ko initialize karein, agar pehle se nahi hua hai
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    # App pehle se initialized hai, dobara na karein
    pass

# Firestore database client ko get karein
db = firestore.client()

def save_study_set(set_name, flashcards, quizzes, summary):
    """
    Current study set ko Firestore mein save karta hai.
    """
    # Ek naya document 'study_sets' collection mein add karein
    doc_ref = db.collection('study_sets').document() # Automatic ID
    doc_ref.set({
        'set_name': set_name,
        'flashcards_json': json.dumps(flashcards),
        'quizzes_json': json.dumps(quizzes),
        'summary_text': summary,
        'created_at': firestore.SERVER_TIMESTAMP # Taaki hum sort kar sakein
    })

def load_all_study_sets():
    """
    Firestore se sabhi study sets ko load karta hai (Collaboration ke liye).
    """
    sets_ref = db.collection('study_sets').order_by('created_at', direction=firestore.Query.DESCENDING).stream()
    
    sets_list = []
    for doc in sets_ref:
        set_data = doc.to_dict()
        sets_list.append({
            "id": doc.id, # Yeh zaroori hai set ko load karne ke liye
            "name": set_data.get('set_name', 'Untitled')
        })
    return sets_list

def load_set_by_id(doc_id):
    """
    Document ID ke zariye ek specific study set ko load karta hai.
    """
    doc_ref = db.collection('study_sets').document(doc_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        return {
            "set_name": data.get('set_name'),
            "flashcards": json.loads(data.get('flashcards_json', '[]')),
            "quizzes": json.loads(data.get('quizzes_json', '[]')),
            "summary": data.get('summary_text', '')
        }
    else:
        print(f"Error: Document with ID {doc_id} not found.")
        return None