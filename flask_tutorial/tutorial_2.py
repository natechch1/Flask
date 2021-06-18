# this tutorial is for the user login, logout and flash message!!!!

from flask import Flask, redirect, url_for, render_template, request,session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(hours=5)


@app.route("/")
def origin():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":   # this is the POST method and post the info to user page
        session.permanent = True
        user = request.form["nm"]   # let user be the info which GET from form tag in login.html
        session["user"] = user  # the "user" after session is the dictionary key
        flash("Login successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")  # this is the GET method to get the info from the login page

@app.route("/user")
def user():
    if "user" in session:  # if the key "user" is in session
        usr = session["user"]
        return render_template("user.html", user=usr)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You are logged out successfully!", "info") # the "info" is the category for this msg
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)