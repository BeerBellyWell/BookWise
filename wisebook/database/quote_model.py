from wisebook import db


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(256), nullable=False)
    book_name = db.Column(db.String(128), nullable=False)
    book_author = db.Column(db.String(128), nullable=False)
    create_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    like = db.Column(db.Integer, default=0, nullable=False)
    # last_update = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    # is_published = db.Column(db.Boolean, default=True)

