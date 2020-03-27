# imports
from flask import Flask
from flask import render_template, url_for, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy
import requests
from urllib import request as rq
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app) # Global variable

class Record(db.Model):

    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer,nullable=False)
    locations = db.Column(db.Integer)

    def __repr__(self):
        return "<Record(name='%s', city='%s', country='%s', count='%s', locations='%s')>" % (self.name, self.city, self.country, self.count, self.locations)

@app.route('/', methods = ['GET', 'POST'])
def home():
    return "Hello!"

@app.route('/refresh', methods = ['GET', 'POST'])
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    db.drop_all()
    db.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db

    url = rq.urlopen('https://api.openaq.org/v1/cities')
    data = url.read()
    new_data = json.loads(data.decode('utf-8'))
    new_data = new_data['results']

    for i in range(len(new_data)):
        row = list()

        for value in new_data[i].values():
            row.append(value)
        row_data = Record(country=row[0], 
        name=row[1], 
        city=row[2], 
        count=row[3], 
        locations=row[4])

        db.session.add(row_data)
    db.session.commit()

    return 'Data refreshed!'   



