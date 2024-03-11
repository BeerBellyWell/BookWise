from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired


class QuoteForm(FlaskForm):
    quote = StringField(
        'Цитата',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 256)]
    )
    book_name = StringField(
        'Название книги',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 128)]
    )
    book_author = StringField(
        'Автор книги',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 128)]
    )
    submit = SubmitField('Добавить')


class RegisterForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 128)]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 60)]
    )
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 128)]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired('Обязательное поле'),
                    Length(1, 60)]
    )
    submit = SubmitField('Войти')
