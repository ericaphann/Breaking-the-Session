
from flask import Flask, render_template, request, redirect, url_for

# Tell Flask where our HTML files are located
app = Flask(__name__, template_folder="Website")


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        # Temporary test login (not real authentication yet)
        if username == "student":
            return redirect(url_for("dashboard"))

        return "Invalid username", 401

    return render_template("login.html")


# Dashboard page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
