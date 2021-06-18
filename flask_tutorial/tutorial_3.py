# this is for the sql database

from flask import Flask, redirect, url_for, render_template, request,session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def origin():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":        # this is the POST method and post the info to user page
        session.permanent = True
        user = request.form["nm"]       # let user be the info which GET from form tag in login.html
        session["user"] = user          # the "user" after session is the dictionary key
        
        found_user = users.query.filter_by(name=user).first()
        if found_user:                                          # if db has this user, save the email in session
            session["email"] = found_user.email
        else:                                                   # if db doesnt have this user name, create one
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        
        flash("Login successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")            # this is the GET method to get the info from the login page

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:  # if the key "user" is in session
        usr = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

            found_user = users.query.filter_by(name=usr).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", user=usr, email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You are logged out successfully!", "info") # the "info" is the category for this msg
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)