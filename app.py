# app.py
from flask import Flask
from flask_cors import CORS
from cards.routes import cards_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(cards_bp)

if __name__ == '__main__':
    app.run(debug=True)