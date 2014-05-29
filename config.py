import os
from authomatic.providers import oauth2

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSF_ENABLED = True
SECRET_KEY = 'You-will-never-guess'

#email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USERNAME = 'kenjin.p@gmail.com'
MAIL_PASSWORD = 'redleg11!1'

# administartor list
ADMINS = ['kenjin.p@gmail.com']

# Authentication Providers
AUTH_PROVIDERS = {

        #google
        'google': {
                'class_': oauth2.Google,

                'consumer_key':'720988641067-npajor51n4cnha48ololvkqtuio08hg0.apps.googleusercontent.com',
                'consumer_secret':'Ds_kOU5kTvgeYVzHFAR1Ei7w',
                'scope':['https://www.googleapis.com/auth/userinfo.profile','email',
                        'https://www.googleapis.com/auth/userinfo.email']

        },
        #linkedin
        'li': {
                'class_': oauth2.LinkedIn,

                'consumer_key':'75w2pqwj422y3z',
                'consumer_secret':'qEK5ZL2c89XRZQYx'
        }
}
