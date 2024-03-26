from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .views import views
    from .auth import auth
    from .functions import functions, Find

    Find.retrieve_restaurants_from_db()


    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(functions, url_prefix = '/')

    from .models import User, Note, Review

    # create_database(app)
    with app.app_context():
        create_database(app)

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        # with app.app_context():
        # create_database(app=app)

        db.create_all()
        print('Created Database!')