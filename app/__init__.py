import os
import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.babel import Babel
from werkzeug import secure_filename
from config import Config, ProdConfig

def create_app(config=ProdConfig):
    app = Flask(__name__, static_url_path='')
    app.config.from_object(config)
    app.debug = app.config['DEBUG']
    register_blueprints(app)
    register_extensions(app)
    register_context_processors(app)
    return app

def register_blueprints(app):
    from app.views import screener
    app.register_blueprint(screener)

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = '/login'

def register_context_processors(app):
    from app.context_processors import (
        inject_static_url,
        inject_example_data,
        inject_template_constants
    )
    app.context_processor(inject_static_url)
    app.context_processor(inject_example_data)
    app.context_processor(inject_template_constants)

db = SQLAlchemy()
bcrypt = Bcrypt()
babel = Babel()
login_manager = LoginManager()

from app import views, models
