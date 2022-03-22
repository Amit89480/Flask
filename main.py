from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


class Contacts(db.Model):
    """
    sno, name phone_num, msg, date, email
    """
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20), nullable=False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, message=message, phone=phone)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


app.run(debug=True)
