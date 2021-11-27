from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os
import ssl
context = ssl.SSLContext()


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

#flask app named app will be created here and config would be set
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


db.init_app(app)

#set up login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

jwt.init_app(app)
mail.init_app(app)

#created database
from .models import User
with app.app_context():
  db.create_all()


#load user from coockie if logged in
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


#blueprints auth routes
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

#non-auth parts
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

#github oauth route
from .github import blueprint as github_blueprint
app.register_blueprint(github_blueprint, url_prefix="/login")

#google oauth route
from .google import blueprint as google_blueprint
app.register_blueprint(google_blueprint, url_prefix="/login")



if __name__ == "__main__":
    app.run()
