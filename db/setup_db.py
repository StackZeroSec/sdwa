from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vuln_db.sqlite"
db = SQLAlchemy(app)

def add_users(db:SQLAlchemy, users):
    for user in users:
        db.session.add(User(username=user['username'],password=hashlib.md5(user['password'].encode('utf-8')).hexdigest(), admin=user["admin"]))
    db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = password
        self.admin = admin


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, default=False, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity



db.create_all()
users = [
    {'username': "user", 'password': "user_password", "admin": False},
    {'username': "user2", 'password': "user2_password", "admin": False},
    {'username': "flask_admin", 'password': "password@123", "admin": True},
]

products = [
    Product("Orange", 1.99, 10),
    Product("Apple", .99, 10),
    Product("Peach", .89, 4),
    Product("Watermelon", 4.5, 6),
    Product("Strawberry", 1.89, 30)
]

add_users(db, users)

for product in products:
    db.session.add(product)
db.session.commit()