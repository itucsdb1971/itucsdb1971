from os import environ


class Config(object):
    WTF_CSRF_ENABLED = True
    PORT = 8080


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get("SECRET_KEY")
    DATABASE_URL = environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"
    DATABASE_URL = "postgres://postgres:docker@localhost:5432/postgres"
