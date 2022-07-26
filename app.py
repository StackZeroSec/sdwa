from crypt import methods
from flask import Flask, render_template, request, session, redirect, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/vuln_db.sqlite"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
Session(app)


@app.route("/")
def home():
    cards = []

    for e in os.listdir("sections"):
        with open(f"sections/{e}/description", "r")as desc_file, open(f"sections/{e}/url", "r") as url_file:
            cards.append(
                {"name": e.capitalize(),
                "image": f"/static/images/{e}.png",
                "description": desc_file.read(),
                "url": url_file.read().strip()}
            )

    return render_template("home.html", cards = cards)
@app.route("/sqli/login", methods= ["GET","POST"])
def sqli_login():
    if "username" in request.form and "password" in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        password = hashlib.md5(password.encode()).hexdigest()

        rs = db.engine.execute("SELECT * from users WHERE username='"+username+"' AND password='"+password+"'").all()

        if len(rs) != 0:
            if rs[0][3] == 1:
                session["admin"] = True
            else:
                session["admin"] = False
            return redirect("/sqli/products")
        else:
            return "Bye bye"
    else:
        return render_template("sqli/login.html")

@app.route("/sqli/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/sqli/login")
@app.route("/sqli/products", methods = ["GET", "POST"])
def sqli_products():
    print(session)
    if "admin" not in session:
        abort(401)
    print(request.form.get("product_name"))
    if "product_name" in request.form:
        rs = db.engine.execute("SELECT * from products WHERE name LIKE'"+request.form.get("product_name")+"%'").all()
    else:
        rs = db.engine.execute("SELECT * from products").all()
    columns = list(rs[0].keys())[1:]

    print(rs)
    return render_template("sqli/products.html", rows=rs, columns=columns)

if __name__ == "__main__":
    app.run()