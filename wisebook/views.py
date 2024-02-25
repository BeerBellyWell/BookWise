from flask import render_template
from wisebook.database.quote_model import Quote
from wisebook import app


@app.route('/')
def hello():
    quotes = Quote.query.all()
    return render_template('index.html', quotes=quotes)
