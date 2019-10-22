from os import environ


class Config(object):
    WTF_CSRF_ENABLED = True
    PORT = 8080

    PASSWORDS = {
        "admin": "$pbkdf2-sha256$29000$PIdwDqH03hvjXAuhlLL2Pg$B1K8TX6Efq3GzvKlxDKIk4T7yJzIIzsuSegjZ6hAKLk",
        "normaluser": "$pbkdf2-sha256$29000$Umotxdhbq9UaI2TsnTMmZA$uVtN2jo0I/de/Kz9/seebkM0n0MG./KGBc1EPw5X.f0",
    }

    ADMIN_USERS = ["admin"]


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get("SECRET_KEY")
    DATABASE_URL = environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "dev"
    DATABASE_URL = "postgres://postgres:docker@localhost:5432/postgres"
