from flask.ext.wtf import Form
from wtforms import TextAreaField, BooleanField, TextField, SubmitField, PasswordField
from wtforms.validators import Required, Length

class TranslationForm(Form):
        to_be_translated = TextAreaField('to_be_translated', validators = [Length(min = 0, max = 500)])
        title_form = TextField('title', validators = [Required()])

class LoginForm(Form):
        nickname_or_email = TextField('Nickname/email', validators = [Required()])
        password = PasswordField('Password', validators = [Required()])
        submit = SubmitField("Login!")

class SignupForm(Form):
        nickname = TextField('Nickname', validators = [Required()])
        email = TextField("Email", validators = [Required()])
        password = PasswordField("Password", validators = [Required()])
        verify_password = TextField("Write Password Again", validators = [Required()])
        submit = SubmitField("Create Account")
