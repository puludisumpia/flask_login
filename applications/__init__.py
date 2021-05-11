from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail, Message

db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "gyhujikop^$oiuythfhguijok"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "votre_email@gmail.com"
    app.config["MAIL_PASSWORD"] = "votre_mot_de_passe"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)

    from applications.blog.views import blog
    from applications.blog.auth import auth

    app.register_blueprint(blog)
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from applications.blog.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

db.create_all(app=create_app())