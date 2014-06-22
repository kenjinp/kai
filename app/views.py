from flask import Flask, render_template, make_response, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import TranslationForm, LoginForm, SignupForm
from models import User, ROLE_USER, ROLE_ADMIN, Order
from datetime import datetime
from collections import Counter
from emails import translation_submit_notification
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from authomatic.providers import oauth2
from config import AUTH_PROVIDERS
#from config import LANGUAGES
#from flask.ext.babel import gettext

maintitle = 'Silly Coffee'
global_price = 0.04
adminpass = 'fartmallow'

authomatic = Authomatic(AUTH_PROVIDERS, 'supser-secret', report_errors=False)

#login_manager user callback method
@lm.user_loader
def load_user(id):
        return User.query.get(int(id))

#main webpage view
@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
        user = g.user
        if user.is_authenticated():
                if user.role == ROLE_ADMIN:
                        orders = Order.query.all()
                else:
                        orders = user.orders
                return render_template("admin.html", orders = orders)
        else:
                form = TranslationForm()
                return render_template("index.html",
		        title = maintitle,
                        form = form
		        )

#orderform view
@app.route('/order-translation', methods = ['GET', 'POST'])
@login_required
def order():
        form = TranslationForm()
        if form.validate_on_submit():
                translation = Order(text = form.to_be_translated.data,
                        timestamp = datetime.utcnow(),
                        title = form.title_form.data,
                        user_id = g.user.id
                        )
                print translation.title
                print translation.text
                db.session.add(translation)
                db.session.commit()
                translation_submit_notification(g.user.email)
                return redirect(url_for("quote", translation_id = translation.id))
        else:
                print "do something else"
        return render_template("order-translation.html",
                metadescription = "lololol",
                title = maintitle,
                form = form)

#view for the price&time quote
@app.route('/quote/<translation_id>', methods = ['GET', 'POST'])
def quote(translation_id):
        translation = Order.query.filter_by(id = translation_id).first()
        words = wordcounter(translation.text)
        cost = words*global_price

        return render_template("quote.html",
                metadescription = "lololol",
                title = maintitle,
                price = global_price,
                words = words,
                cost = cost)

#view to see a specific translation order
@app.route('/orderid/<translation_id>')
def orderid(translation_id):
        order = Order.query.filter_by(id=translation_id).first()
        orderer = User.query.filter_by(id=order.user_id).first()
        print order.title
        return render_template("orderid.html",
                order = order,
                orderer = orderer)

#view to see all the orders someone has (admin can see all)
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
        pass

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
        form = SignupForm()
        if form.validate_on_submit():
                password = form.password.data
                print 'password is %r'%password
                print 'signupformvalidated'
                user = User.query.filter_by(email = form.email.data).first()
                if user is None:
                        print"user is none"
                        user = User(nickname = User.make_unique_nickname(form.nickname.data),
                                        email = form.email.data,
                                        role = ROLE_USER)
                        user.set_password(password)
                        db.session.add(user)
                        db.session.commit()
                login_user(user)
                print '%r is now logged in'%user.nickname
                flash('Welcome to Silly Coffee!')
                return redirect(url_for("index"))
        else:
                print 'this is soemthing that goes when nothing happesn in signup'
        return render_template("signup.html", form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
                print 'loginformvalidated'
                user = User.query.filter_by(nickname = form.nickname_or_email.data).first()
                if user.check_password(form.password.data) == True:
                        login_user(user)
                        flash('Succesfully Logged-in!')
                else:
                        flash('incorrect nickname/password combo')
                        return redirect(url_for('login'))
                return redirect(url_for("index"))
        else:
                print 'I dont know what this does'
        return render_template("login.html", form = form)

# Oauth v2 authentication view
@app.route('/login/<provider_name>', methods = ['GET', 'POST'])
def auth(provider_name):
        if g.user is not None and g.user.is_authenticated():
                flash("You're already logged-in, bustah!")
                return redirect(request.args.get('next') or url_for('index'))

        response = make_response()

        result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
        print 'making response to provider'
        print result
        if result:
                print "result has been made"
                if result.user:
                        result.user.update()
                        print 'user updated'
                if result.user.email is None or result.user.email =="":
                        flash('Invalid Login. Please try again.')
                        print 'invalid login'
                        return redirect(url_for('index'))
                user = User.query.filter_by(email = result.user.email).first()
                if user is None:
                        print "user is none"
                        nickname = result.user.name
                        if nickname is None or nickname == "":
                                nickname = result.user.email.split('@')[0]
                        nickname = User.make_unique_nickname(nickname)
                        user = User(nickname = nickname,
                                         email = result.user.email,
                                         role = ROLE_USER)
                        db.session.add(user)
                        db.session.commit()
                        print 'put user in database, nickname: ' + nickname
                print 'loging %s in'%user.nickname
                login_user(user)
                print 'loggeed %s in succesfully'%user.nickname
                return redirect(url_for('index'))
        return response
        print response

#logout
@app.route('/logout')
@login_required
def logout():
        logout_user()
        print 'logged someone out'
        flash('Successfully logged out.')
        return redirect(url_for('index'))

#login_manager g set-up method
@app.before_request
def before_request():
        g.user = current_user
        if g.user.is_authenticated():
                g.user.last_seen = datetime.utcnow()
                db.session.add(g.user)
                db.session.commit()

#this might not be important (word counter)
def wordcounter(words_to_count):
        words = words_to_count.split()
        wordCount = 0
        for w in words:
                wordCount+=1
        return float(wordCount)

#Error Handlers
@app.errorhandler(404)
def not_found_error(error):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
