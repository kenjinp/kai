from flask import render_template, flash, redirect
from app import app
from forms import TranslationForm
#from config import LANGUAGES
#from flask.ext.babel import gettext


#This is the main page of the website (home)
@app.route('/')
@app.route('/index')
def index():
        form = TranslationForm()
	if form.validate_on_submit():
                print "do something"
                return redirect(url_for('quote'))
        else:
                print "do something else"
        return render_template("index.html",
		title = 'Silly Coffee',
                form = form
		)

@app.route('/quote')
def quote():
        pass
        #some interesting math goes here
#@babel.localselector
#def get_locale():
#        return request.accept_languages.best_match(LANGUAGES.keys()
