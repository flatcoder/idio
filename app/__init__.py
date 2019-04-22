from flask import Flask, request
from flask_restful import Api
from app.config import app_config

def create_app(env_name, db):
    from app.api import UrlsAPI
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    api = Api(app)
    api.add_resource(UrlsAPI, '/api/urls')
    db.init_app(app)
    # db.create_all()
    return app
