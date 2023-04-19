import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = 1
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Swagger(object):
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.yaml'