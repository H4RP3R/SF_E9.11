import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aido2aGhielu0yuopieXoosoch6pheiV'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'event_planner.py'
