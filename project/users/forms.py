from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(Form):
    name = StringField('Username', validators=[DataRequired(), Length(min=6, max=26)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=26)])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password', message='Password must match!')]
    )


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
