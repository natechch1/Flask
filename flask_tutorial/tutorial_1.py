from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/w3school")
def w3school():
    return render_template("w3school.html",)

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/new")
def new_page():
    return render_template("new.html",)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":   # this is the POST method and post the info to user page
        user = request.form["nm"]   # let user be the info which GET from form tag in login.html
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")  # this is the GET method to get the info from the login page

@app.route("/<usr>")
def user(usr):
    return f"<h1>User's name is {usr}</h1>"


# @app.route("/<name>")
# def home(name):
#     return render_template("index.html", content=name, r=20, name_list=["hong","ce", "chen"])

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

# @app.route("/admin")
# def admin():
#     return redirect(url_for("user",name="Admin"))

if __name__ == '__main__':
    app.run(debug=True)
