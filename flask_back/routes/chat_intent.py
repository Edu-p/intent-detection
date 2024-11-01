from flask import request, jsonify, Blueprint
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from sklearn.preprocessing import LabelEncoder
import pickle

chat_intent_bp = Blueprint('chat_intent', __name__)

def predict_intent(tokenizer, model, label_encoder,  text:str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = outputs.logits.softmax(dim=1)
    pred_label = torch.argmax(probs).item()
    intent = label_encoder.inverse_transform([pred_label])
    return intent[0]


@chat_intent_bp.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    user_id = data['user_id']
    content = data['content']
    
    # Load resources to predict intent
    tokenizer = AutoTokenizer.from_pretrained('./utils/rsc/tokenizer')
    model = AutoModelForSequenceClassification.from_pretrained('./utils/rsc/model')
    
    with open('./utils/rsc/label_encoder/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)

    predicted_intent = predict_intent(tokenizer=tokenizer, model=model, label_encoder=label_encoder, text=content)
    print(f"Predicted Intent: {predicted_intent}")

    # TODO: switch case for what to do with intent

    return jsonify({'predicted_intent': predicted_intent})





