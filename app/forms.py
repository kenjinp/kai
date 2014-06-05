from flask.ext.wtf import Form
from wtforms import TextAreaField, BooleanField, TextField, SubmitField, PasswordField
from wtforms.validators import Required, Length
from app.models import User
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
        verify_password = PasswordField("Confirm your Password", validators = [Required()])
        submit = SubmitField("Create Account")

        def __init__(self, *args, **kwargs):
                Form.__init__(self, *args, **kwargs)

        def validate(self):
                if not Form.validate(self):
                        return False
                if self.password.data != self.verify_password.data:
                        self.verify_password.errors.append('Your passwords don\'t match!')
                        return False
                user = User.query.filter_by(nickname = self.nickname.data).first()
                if user != None:
                        self.nickname.errors.append('This nickname is already in use. Please Choose Another.')
                        return False
                user_email = User.query.filter_by(email = self.email.data).first()
                if user_email != None:
                        self.email.errors.append('This email is already in use. Maybe you meant to login?')
                        return False
                return True
