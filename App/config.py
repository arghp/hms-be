from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()
secret_key = os.urandom(24)

class Config:
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/hotel_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test'


def create_app(config_name='default', main_bp=None):  # Add main_bp as a parameter
    app = Flask(__name__)
    # Configurations
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    if main_bp:
        app.register_blueprint(main_bp)

    return app

