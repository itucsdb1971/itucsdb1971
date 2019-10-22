from os import environ


class Config(object):
    WTF_CSRF_ENABLED = True
    PORT = 8080


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'
