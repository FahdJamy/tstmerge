import os

from flask import Flask
from flask_restplus import Api
from monster.config import Config


api = Api()

secret = os.environ.get('SECRET_KEY')
print (secret)

def app_creator(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	app.config['SECRET_KEY'] = 'thisistoosecret'
	api.init_app(app)

	return app

from monster import routes

@api.errorhandler
def  sever_error_handler(error):
	return {'message' : str(error)}, getattr(error,  'code', 500)