#!env/bin/ python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# The main database class
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.String(120), unique=True)

    def __init__(self, title, body):
        self.title = title
        self.body = body

# The addnote function which adds the notes to the database.
def addnote(title='', body=''):
    newnote = Note(title, body)
    db.add(newnote)
    db.commit()


