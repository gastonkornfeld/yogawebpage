from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

# init database
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
mail_manager = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjh kjshkjdhjs'
    basedir = path.abspath(path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + path.join(basedir, 'app.sqlite')
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    mail_manager.init_app(app)

    from .views import views
    from .auth import auth
   

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
     
    from .models import User, YogaPost, Recipe, Course, Email_user, Message, Category
    
    

    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app

