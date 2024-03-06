from flask import render_template
from wisebook.database.quote_model import Quote
from wisebook import app
from wisebook.forms import QuoteForm


@app.route('/')
def hello():
    # quotes = Quote.query.all()
    return render_template('index.html') #quotes=quotes)


@app.route('/add_quote')
def add_quote():
    form = QuoteForm()
    return render_template('add_quote.html', form=form)
