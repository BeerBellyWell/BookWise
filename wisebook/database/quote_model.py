from flask_login import UserMixin

from wisebook import db


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(256), nullable=False)
    book_name = db.Column(db.String(128), nullable=False)
    book_author = db.Column(db.String(128), nullable=False)
    create_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    like = db.Column(db.Integer, default=0, nullable=False)
    # добавить поля last_update и is_published, а также FK


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
