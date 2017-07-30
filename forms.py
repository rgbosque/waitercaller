# FOR WTForms 2.1 VERSION
# from flask_wtf import FlaskForm
# from wtforms import PasswordField
# from wtforms import SubmitField
# from wtforms import validators
# from wtforms.fields.html5 import EmailField

# FOR WTForms 3 VERSION
from wtforms import Form, PasswordField, SubmitField, TextField, HiddenField, validators
from wtforms.fields.html5 import EmailField


class RegistrationForm(Form):
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


class LoginForm(Form):
    loginemail = EmailField('email',
                            validators=[
                                validators.DataRequired(),
                                validators.Email()
                            ])
    loginpassword = PasswordField('password',
                                  validators=[
                                      validators.DataRequired(message="Password field is required")
                                  ])
    submit = SubmitField('submit', [validators.DataRequired()])


class CreateTableForm(Form):
    tablenumber = TextField('tablenumber', [validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])


class DeleteTableForm(Form):
    tableid = HiddenField('tableid', [validators.DataRequired()])
    submit = SubmitField('delete', [validators.DataRequired()])
