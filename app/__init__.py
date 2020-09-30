from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config_options
from flask_mail import Mail

app = Flask(__name__)

db = SQLAlchemy(app)
login_manager = LoginManager()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
   

    # Registering blueprints
    

    return app