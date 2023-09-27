from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "account_system"  # Change the DB_NAME to match your database name

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '@Antony1237'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://account_dev:account_pwd@localhost/account_system'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views  # Import your views (app.py) instead of app
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')  # Use a different URL prefix for auth

    from .models.account import Account
    from .models.base_model import BaseModel
    from .models.transaction import Transaction
    from .models.user import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = User.query.get(str(id))
        return user

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
