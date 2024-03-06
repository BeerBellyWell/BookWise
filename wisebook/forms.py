from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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
    