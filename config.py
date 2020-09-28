import os


POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aido2aGhielu0yuopieXoosoch6pheiV'
    SQLALCHEMY_DATABASE_URI = \
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'event_planner.py'
