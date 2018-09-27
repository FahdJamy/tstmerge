import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config ():

	SECRET_KEY = os.getenv('SECRET_KEY')
	DEBUG = True

class TestConfig (Config):
	DATABASE = 'test'
	pass