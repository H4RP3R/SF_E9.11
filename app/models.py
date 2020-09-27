from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='author', lazy='dynamic')

    def __str__(self):
        return f'<User: {self.username} | id: {self.id}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, index=True, unique=False, nullable=False)
    end = db.Column(db.DateTime, index=True, unique=False, nullable=False)
    theme = db.Column(db.String(128))
    description = db.Column(db.String(512))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return f'<Event id: {self.id} (start: {self.start} end: {self.end})>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
