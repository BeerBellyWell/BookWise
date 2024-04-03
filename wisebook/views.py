import os

from flask import render_template, redirect, url_for, jsonify, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from wisebook.database.models import Quote, User, Like
from wisebook import app, db, login_manager
from wisebook.forms import QuoteForm, RegisterForm, LoginForm


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Quote': Quote,
            'User': User, 'Like': Like}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    quotes = Quote.query.order_by(Quote.create_at.desc()).all()
    return render_template('pages/index.html', quotes=quotes)


@app.route('/add_quote', methods=['GET', 'POST'])
@login_required
def add_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = Quote(
            quote = form.quote.data,
            book_name = form.book_name.data,
            book_author = form.book_author.data,
            user_id = current_user.id
        )
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pages/add_quote.html', form=form)


@app.route('/like_quote/<int:quote_id>', methods=['POST', 'GET'])
@login_required
def like_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    like = Like.query.filter_by(user_id=current_user.id, quote_id=quote.id).first()
    if like:
        db.session.delete(like)
        quote.like_count -= 1
        db.session.commit()
        context = {
            'message': 'Лайк убран',
            'like_count': quote.like_count
        }
        return jsonify(context)
    else:
        new_like = Like(user_id=current_user.id, quote_id=quote.id)
        quote.like_count += 1
        db.session.add(new_like)
        db.session.commit()
        context = {
            'message': 'Лайк поставлен',
            'like_count': quote.like_count
        }
        return jsonify(context)


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
        flash('Неверное имя пользователя или пароль', 'error')
    return render_template('pages/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    users_quotes = Quote.query.filter_by(user_id=user.id).order_by(Quote.create_at.desc()).all()
    return render_template('pages/profile.html', users_quotes=users_quotes, user=user)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_avatar', methods=['POST', 'GET'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['avatar']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
        # return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
        current_user.avatar_filename = filename
        db.session.commit()
        flash('Avatar uploaded successfully')
        return redirect(url_for('profile', username=current_user.username))
    else:
        flash('Invalid file type')
        return redirect(request.url)