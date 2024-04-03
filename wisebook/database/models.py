from flask_login import UserMixin

from wisebook import db


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(256), nullable=False)
    book_name = db.Column(db.String(128), nullable=False)
    book_author = db.Column(db.String(128), nullable=False)
    create_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    like_count = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # добавить поля last_update и is_published
    likes = db.relationship('Like', backref='quote', lazy=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    avatar_filename = db.Column(db.String(100), nullable=True)
    quotes = db.relationship('Quote', backref='author', lazy=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
        'user_id', 'quote_id', name='_user_quote_uc'),
        )
