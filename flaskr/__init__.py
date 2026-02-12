from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_tutorial.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Is used to encrypt tokens and determine their validity
    app.config["JWT_SECRET_KEY"] = "4iEEBkfSzWHLNeuuz9kUTg=="

    app.config["PROPAGATE_EXCEPTIONS"] = True

    return app
