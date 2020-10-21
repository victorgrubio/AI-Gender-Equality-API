from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASS')
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = os.getenv('DB_NAME_DEV')
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DB_NAME = os.getenv('DB_NAME_DEV')
    SESSION_COOKIE_SECURE = False
