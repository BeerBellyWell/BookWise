from wisebook import db


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(256), nullable=False)
    book_name = db.Column(db.String(128), nullable=False)
    book_author = db.Column(db.String(128), nullable=False)
    create_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    like = db.Column(db.Integer, default=0, nullable=False)
    # добавить поле last_update и is_published

