from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from wisebook.database.quote_model import Quote, User
from wisebook import app, db, login_manager
from wisebook.forms import QuoteForm, RegisterForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    quotes = Quote.query.all()
    return render_template('pages/index.html', quotes=quotes)


@app.route('/add_quote', methods=['GET', 'POST'])
@login_required
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256'
        )
        user = User(
            username = form.username.data,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('pages/register.html', form=form)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        return render_template('pages/login.html', form=form)
    return render_template('pages/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('pages/index.html')
    # return render_template('pages/logout.html')
