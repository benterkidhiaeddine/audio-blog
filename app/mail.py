from threading import Thread
from flask import render_template
from flask_mail import Message
from app import mail,app
import os


def async_email_send(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(user):

    token = user.generate_reset_token()

    msg = Message()
    msg.subject = "Flask App Password Reset"
   
    msg.sender = "thekizzer.swag@gmail.com"
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html', user=user, token=token)
    thr = Thread(target=async_email_send,args=[app,msg])
    thr.start()
    print("this executes")