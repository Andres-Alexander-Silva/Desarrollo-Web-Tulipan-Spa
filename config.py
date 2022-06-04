import os

class Config(object):
    SECRET_KEY = "myScretKeyTulipanSpaAndresSilva"
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:andres2611@localhost:5432/TulipanSpa"