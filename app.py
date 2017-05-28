#!env/bin/ python

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# The main database class
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.String(120), unique=True)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Note u %r>' % (self.title)

# The addnote function which a dds the notes to the database.
def addnote(title='', body=''):
    newnote = Note(title, body)
    db.session.add(newnote)
    db.session.commit()

# Just for testing. Unneeded as it can be skipped.
def viewall():
    notes = Note.query.all()
    for note in notes:
        print(note.title)

# delete the note
def delnote(noteid):
    Note.query.filter(Note.id == noteid).delete()
    db.session.commit()


@app.route('/')
def view():
    return render_template("new.html", results = Note.query.all())

# view every note asid based on the note's id on the db.
@app.route('/<int:userid>', methods=["GET", "POST"])
def viewnote(userid):
    getnote = Note.query.get_or_404(userid)
    return render_template("note.html", getnote=getnote)

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return redirect("/")
    else:
        title = request.form["title"]
        body = request.form["body"]
        note = Note(title, body)
        db.session.add(note)
        db.session.commit()
        return redirect("/")

@app.route("/del", methods=["POST"])
def delete():
    note = request.form["delbuttn"]
    delnote(note)
    return redirect("/")

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
