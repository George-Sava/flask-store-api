from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, '.env'))

class Config:
    
    SECRET_KEY = environ.get('SECRET_KEY')
    DATABASE_USERNAME = environ.get('DATABASE_USERNAME')
    DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
    DATABASE_HOSTNAME = environ.get('DATABASE_HOSTNAME')
    DATABASE_PORT = environ.get('DATABASE_PORT')
    DATABASE_NAME = environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}'
    ALGORITHM = environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ALGORITHM = ALGORITHM
    
    
class DevConfig(Config):
    
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/docs'
    API_URL = 'http://127.0.0.1:5000'

class ProdConfig(Config):
    
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SWAGGER_URL = '/docs'
    API_URL = 'https://store-chain-rest-api.herokuapp.com/'
    
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///E:\\API Dev\\API Courses\\Udemy\\Rest API Python Flask standard\\flask_API_Store_v1_1\\data.db'    