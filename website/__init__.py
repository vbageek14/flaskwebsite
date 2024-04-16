from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from website import config
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# Initializes the database
db = SQLAlchemy()
DB_NAME = "database.db"

# Creates Flask application instance
app = Flask(__name__)

def create_app():
    app = Flask(__name__)

    # Set up security configurations for the application such as to protect against CRSF
    csrf = CSRFProtect(app)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # Configures SQLAlchemy database URI and initialize database instance
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    # Configures Flask-Login within the application
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Defines a user loader function that Flask-Login will use to load user objects from the database for authentication purposes
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Defines configuration settings for the password reset feature
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = config.EMAIL_USER
    app.config['MAIL_PASSWORD'] = config.EMAIL_PASS

    # Initializes Flask-Mail extension
    mail = Mail(app)

    # Injects SearchForm into all templates in the application
    @app.context_processor
    def base():
        from .webforms import SearchForm
        form = SearchForm()
        return dict(form=form)
    
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")
