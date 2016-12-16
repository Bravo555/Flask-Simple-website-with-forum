from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

app.secret_key = "E5CDD5E9422A8D509A392DB9621097C2DEFF1C1AE90714A78AC84E3EAC072E87" #remember to change it!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.Text)
    password = db.Column('password', db.Text)
    email = db.Column('email', db.Text)

@app.route("/")
def index():
    return render_template("index.html", p=1)

@app.route("/forum")
def forum():
    return "Work in progress"

@app.route("/panel")
def panel():
    if session.get('logged_in') == True:
        return render_template("panel.html", p=4, user=User.query.filter_by(username = session['username']).one_or_none())

    return render_template("login.html", p=3)

@app.route("/login", methods=['POST'])
def login():
    _username = request.form['username']
    _passwd = request.form['passwd']

    user = User.query.filter_by(username = _username).one_or_none()

    if(user == None):
        flash(u"User doesn't exist")
        return redirect(url_for('panel'))
    elif(user.password != hashlib.sha1(_passwd.encode("UTF-8")).hexdigest()):
        flash(u'Incorrect password')
        return redirect(url_for('panel'))
    else:
        session['username'] = _username
        session['logged_in'] = True
        return redirect(url_for('panel'))

@app.route("/register", methods=['POST'])
def register():
    _username = request.form['username']
    _passwd = request.form['passwd']
    _passwdcheck = request.form['passwdcheck']
    _email = request.form['email']

    if(_passwd != _passwdcheck or len(_passwd) < 6):
        flash(u'Incorrect password')
        return redirect(url_for('panel'))

    if(User.query.filter_by(username = _username).one_or_none() != None and User.query.filter_by(email = _email).one_or_none() != None):
        flash(u'Username or email already in use')
        return redirect(url_for('panel'))

    new_user = User(username = _username, password = hashlib.sha1(_passwd.encode("UTF-8")).hexdigest(), email = _email) #poor hashing is a placeholder for now
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route("/logout")
def logut():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='', port=80)
