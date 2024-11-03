from flask import request, jsonify, Blueprint
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from sklearn.preprocessing import LabelEncoder
import pickle
from db import db
from typing import Tuple

chat_intent_bp = Blueprint('chat_intent', __name__)

UNKNOWN_PROMPT = "Please, I didn't understand well, could you send your intent again?"
RETRIEVE_LAST_THREE_PROMPT = "Here are your last three intents stored in our database:\n\n{tuple_docs}"
PREDICT_INTENT_PROMPT = "Predicted intent of the last message: {predicted_intent}"
threshold = 0.605 # find_best notebook 


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
    user_name = data['user_name']
    content = data['content']
    
    # load resources to predict intent
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
            final_prompt = UNKNOWN_PROMPT
        case "RetrieveLastThree":
            last_docs = list(db.Intents.find({"user_name": user_name}).sort('_id', -1).limit(3))
            index_mapping = {0: "Last", 1: "Second to last", 2: "Third to last"}
            
            tuple_docs = [(index_mapping.get(i, f"Document {i+1}"), doc['intent']) for i, doc in enumerate(last_docs)]
            intents_str = "\n".join([f"{index} -> {intent}" for index, intent in tuple_docs])
            final_prompt = RETRIEVE_LAST_THREE_PROMPT.format(tuple_docs=intents_str)

            db.Intents.insert_one({
                "user_name":user_name,
                "intent":predicted_intent
            })

        case _:
            final_prompt = PREDICT_INTENT_PROMPT.format(predicted_intent=predicted_intent)
            db.Intents.insert_one({
                "user_name":user_name,
                "intent":predicted_intent
            })


    return jsonify({'model_response': final_prompt})