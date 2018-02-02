from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from werkzeug.contrib.fixers import ProxyFix

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    # Set up for nginx if using proxy server when deployment
    #app.wsgi_app = ProxyFix(app.wsgi_app)
    return app