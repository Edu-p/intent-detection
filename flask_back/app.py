from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.chat_intent import chat_intent_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# setup mongo 

# register blueprints
app.register_blueprint(chat_intent_bp) 

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

