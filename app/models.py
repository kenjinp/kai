from app import db
from werkzeug import generate_password_hash, check_password_hash

#USER STUFF

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_TRANSLATOR = 2

class User(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nickname = db.Column(db.String(64), index = True, unique = True)
        email = db.Column(db.String(120), index = True, unique = True)
        role = db.Column(db.SmallInteger, default = ROLE_USER)
        orders = db.relationship('Order', backref = 'customer', lazy = 'dynamic')
        last_seen = db.Column(db.DateTime)
        pwdhash = db.Column(db.String(54))

        def is_authenticated(self):
                return True

        def is_active(self):
                return True

        def is_anonymous(self):
                return False

        def get_id(self):
                return unicode(self.id)

        def __repr__(self):
                return '<user %r>'%(self.email)

        def set_password(self, password):
                self.pwdhash = generate_password_hash(password)

        def check_password(self, password):
                return check_password_hash(self.pwdhash, password)

        @staticmethod
        def make_unique_nickname(nickname):
                if User.query.filter_by(nickname = nickname).first() == None:
                        return nickname
                version = 2
                while True:
                        new_nickname = nickname + str(version)
                        if User.query.filter_by(nickname = new_nickname).first() == None:
                                break
                        version += 1
                return new_nickname

#TRANSLATIO ORDER STUFF

STATUS_PENDING = 0
STATUS_AWAITING_APPROVAL = 1
STATUS_COMPLETED = 2

class Order(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        title = db.Column(db.String(64), index = True)
        text = db.Column(db.String(1000))
        price = db.Column(db.Float)
        timestamp = db.Column(db.DateTime)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        status = db.Column(db.SmallInteger, default = STATUS_PENDING)

        def __repr__(self):
                return '<Order %r>' % (self.id)
