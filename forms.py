from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class RegistrationForm(FlaskForm):
    email = EmailField('email',
                       validators=[
                           validators.DataRequired(),
                           validators.Email()
                       ]
                       )
    password = PasswordField('password',
                             validators=[
                                 validators.DataRequired(),
                                 validators.Length(
                                     min=8,
                                     message="Please choose a password of atleast 8 character"
                                 )
                             ])
    password2 = PasswordField('password2',
                              validators=[
                                  validators.DataRequired(),
                                  validators.EqualTo('password', message="Password must match")
                              ])
    submit = SubmitField('submit', [validators.DataRequired()])
