from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clau-super-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
# login_manager = LoginManager(app)

from app import routes
