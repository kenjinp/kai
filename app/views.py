from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import TranslationForm, LoginForm
from models import User, ROLE_USER, ROLE_ADMIN, Order
from datetime import datetime
from collections import Counter

#from config import LANGUAGES
#from flask.ext.babel import gettext

maintitle = 'Silly Coffee'
global_price = 0.04
adminpass = 'fartmallow'
#This is the main page of the website (home)

@lm.user_loader
def load_user(id):
        return User.query.get(int(id))

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
        user = g.user
        form = TranslationForm()
        return render_template("index.html",
		title = maintitle,
                form = form
		)

@app.route('/order-translation', methods = ['GET', 'POST'])
def order():
        form = TranslationForm()
        if form.validate_on_submit():
                translation = Order(text = form.to_be_translated.data,
                        timestamp = datetime.utcnow(),
                        email = form.email_form.data,
                        title = form.title_form.data
                        )
                print translation.title
                print translation.text
                db.session.add(translation)
                db.session.commit()
                return redirect(url_for("quote"))
        else:
                print "do something else"
        return render_template("order-translation.html",
                metadescription = "lololol",
                title = maintitle,
                form = form)

@app.route('/quote', methods = ['GET', 'POST'])
def quote(translation):
        words = wordcounter(translation.text)
        cost = words*global_price

        return render_template("quote.html",
                metadescription = "lololol",
                title = maintitle,
                price = global_price,
                words = words)

@app.route('/orderno/<translation_id>')
def orderid(translation_id):
        order = Order.query.filter_by(id=translation_id).first()
        print order.title
        return render_template("orderid.html",
                order = order)

@app.route('/admin', methods = ['GET', 'POST'])
@login_required
def admin():
        print "made it to login page"
        orders = Order.query.all()
        return render_template("admin.html", orders = orders)

@app.route('/login', methods = ['GET', 'POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
                if form.password.data == adminpass:
                        print "passwords match"
                        login_user(current_user)
                        return redirect(url_for('admin'))
                else:
                        flash('Wrong Password')
                        print "wrong password"
                        return redirect(url_for('index'))
        return render_template("login.html",
                                form = form,
                                title = maintitle)

@app.before_request
def before_request():
        g.user = current_user

def wordcounter(words_to_count):
        words = words_to_count.split()
        wordCount = Counter(words)
        return wordCount

        #some interesting math goes here
#@babel.localselector
#def get_locale():
#        return request.accept_languages.best_match(LANGUAGES.keys()
