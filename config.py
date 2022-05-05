import os

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# for .env when ready
# SQLALCHEMY_DATABASE_URI = postgresql://ixdtvyum:0JymrgSJgluB68ONxkz5xKnWH_syKiiA@otto.db.elephantsql.com/ixdtvyum
# SQLALHEMY_TRACK_MODIFICATIONS = False 