from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import true
from Server.utils import append_parent_dir
from datetime import timedelta

append_parent_dir()

from privates import *



db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = APP_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.permanent_session_lifetime = timedelta(minutes=5)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .DBModels import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(u):
        return User.query.get(int(u))

    return app


def create_database(app):
    if not path.exists('WebInterface/' + DB_NAME):
        db.create_all(app=app)
        print("Database created")
