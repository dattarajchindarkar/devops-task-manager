import os
from flask import Flask
from .routes import api


def create_app():
    app = Flask(__name__)

    app.config["APP_NAME"] = os.getenv("APP_NAME", "DevOps Task Manager")
    app.config["APP_ENV"] = os.getenv("APP_ENV", "development")
    app.config["APP_VERSION"] = os.getenv("APP_VERSION", "1.0.0")

    app.register_blueprint(api)

    return app
