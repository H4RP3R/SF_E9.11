import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aido2aGhielu0yuopieXoosoch6pheiV'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') \
        or 'postgresql://postgres:docker@localhost:5432/events_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
