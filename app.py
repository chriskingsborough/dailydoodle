from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from datetime import datetime
from config import Config
from artprompts.models import db
from artprompts.models import User
# import random

app = Flask(__name__)
app.config.from_object(Config)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from artprompts import routes

if __name__ == '__main__':
    app.run(debug=True)
