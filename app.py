from flask import Flask, request
from flask_mail import Mail, Message

import os


app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hello, World!"



app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/send_email')
def send_email():
    msg = Message('Prova Oggetto', sender='monacodaniele1990@live.it', recipients=['monacodaniele1990@live.it'])
    msg.body = "Questo è il testo dell'email."
    mail.send(msg)
    return "Email inviata!"

if __name__ == '__main__':
    app.run(debug=True)
