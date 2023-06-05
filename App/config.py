from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
secret_key = os.urandom(24)

def create_app():
    app = Flask(__name__)
    # Configurations
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ekkasak@localhost:5432/hotel_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
