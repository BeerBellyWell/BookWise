from flask import render_template, redirect, url_for
from wisebook.database.quote_model import Quote
from wisebook import app, db
from wisebook.forms import QuoteForm


@app.route('/')
def index():
    quotes = Quote.query.all()
    return render_template('pages/index.html', quotes=quotes)


@app.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = Quote(
            quote = form.quote.data,
            book_name = form.book_name.data,
            book_author = form.book_author.data
        )
        
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pages/add_quote.html', form=form)


@app.route('/test')
def test_html():
    return render_template('test.html')
