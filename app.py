from crypt import methods
from flask import Flask, render_template, request, session, redirect, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
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

@app.route("/xss/list")
def xss_list():
    return render_template("xss/xss_list.html")

@app.route("/xss/reflected")
def xss_reflected():
    name = request.args.get('name')
    if name == None:
        name = "Anonymous"
    return render_template("/xss/reflected.html", name=name)

@app.route("/xss/stored", methods=["GET", "POST"])
def xss_stored():

    db_file = "comments.txt"

    file = Path(db_file)
    file.touch(exist_ok=True)

    if request.method == 'POST':
        comment = request.form["comment"]

        with open(db_file, "a") as f:
            f.write(comment+"\n")

    comments = ""
    with open(db_file, "r+") as f:
        comments = f.readlines()

    return render_template("/xss/stored.html", comments=comments)

@app.route("/xss/stored/clear")
def xss_stored_clear():
    db_file = "comments.txt"

    file = Path(db_file)
    if file.exists():
        file.unlink()
    return redirect("/xss/stored")

@app.route("/xss/dom")
def xss_dom_based():
    return render_template("xss/dom.html")


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
            return "Login failed"
    else:
        return render_template("sqli/login.html")

@app.route("/sqli/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/sqli/login")

@app.route("/sqli/products", methods = ["GET", "POST"])
def sqli_products():

    if "admin" not in session:
        abort(401)

    message = "You are logged in as admin, congratulation!" if session["admin"] else "You are logged in as normal user"
    if "product_name" in request.form:
        rs = db.engine.execute("SELECT * from products WHERE name LIKE'"+request.form.get("product_name")+"%'").all()
    else:
        rs = db.engine.execute("SELECT * from products").all()
    columns = list(rs[0].keys())[1:]


    return render_template("sqli/products.html", rows=rs, columns=columns, message=message)

@app.route("/cmdi")
def cmdi():
    sites = os.listdir("static/sites")
    current_site = None
    if request.args.get("current_site") != None:
        site = request.args.get("current_site")
        description = os.popen(f"cat static/sites/{site}").read()
        current_site = {
            "name": site.capitalize(),
            "description": description
        }
    return render_template("cmdi/cmdi.html", sites=sites, current_site=current_site)

if __name__ == "__main__":
    app.run()