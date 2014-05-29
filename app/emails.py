from flask.ext.mail import Message
from app import app,mail
from config import ADMINS
from flask import render_template
from threading import Thread
from decorators import async

@async
def send_async_email(msg):
        with app.app_context():
                mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender = sender, recipients = recipients)
        msg.body = text_body
        msg.html = html_body
        send_async_email(msg)

def translation_submit_notification(email):
        recipients = []
        recipients.append(email)
        print "notification email sent?"
        send_email("Silly Coffee we're working on it!",
                ADMINS[0],
                recipients,
                render_template("translation_submit_notification.txt"),
                render_template("translation_submit_notification.html"))

