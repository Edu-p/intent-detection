from flask import request, jsonify, Blueprint
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from sklearn.preprocessing import LabelEncoder
import pickle
from db import db
from typing import Tuple

chat_intent_bp = Blueprint('chat_intent', __name__)

threshold = 0.5

def predict_intent(tokenizer, model, label_encoder,  text:str) -> Tuple[str, float]:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = outputs.logits.softmax(dim=1)
    pred_label = torch.argmax(probs).item()
    score = probs[0, pred_label].item()
    intent = label_encoder.inverse_transform([pred_label])
    return intent[0], score


@chat_intent_bp.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    user_id = data['user_id']
    content = data['content']
    
    # Load resources to predict intent
    tokenizer = AutoTokenizer.from_pretrained('./rsc/tokenizer')
    model = AutoModelForSequenceClassification.from_pretrained('./rsc/model')
    
    with open('./rsc/label_encoder/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)

    predicted_intent, score = predict_intent(tokenizer=tokenizer, model=model, label_encoder=label_encoder, text=content)
    if score < threshold:
        predicted_intent = "Unknown"

    # dealing with intents
    match predicted_intent:
        case "Unknown":
            pass
        case "RetrieveLastThree":
            last_docs = list(db.Intents.find().sort('_id', -1).limit(3))
            tuple_docs = [(i, doc['intent']) for i, doc in enumerate(last_docs)] # 0 -> most recent
            print(tuple_docs)

            db.Intents.insert_one({
                "user_id":user_id,
                "intent":predicted_intent
            })
        case _:
            db.Intents.insert_one({
                "user_id":user_id,
                "intent":predicted_intent
            })


    return jsonify({'predicted_intent': predicted_intent})