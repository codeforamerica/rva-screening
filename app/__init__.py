import os
import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.babel import Babel
from werkzeug import secure_filename
from config import Config

app = Flask(__name__, static_url_path='')

app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
# unless we are in a production environment, turn on debug
app.debug = app.config['SCREENER_ENVIRONMENT'] != 'prod'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
babel = Babel(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)
app.logger.addHandler(handler)

@app.context_processor
def inject_template_constants():
    """Adds variables to template context.
    """
    from app import example_data, template_constants
    # get static url
    static_url = os.environ.get('STATIC_URL', app.static_url_path)
    if not static_url.endswith('/'):
        static_url += '/'
    # add static_url, CONSTANTS, & EXAMPLE
    return dict(
        static_url=static_url,
        CONSTANTS=template_constants,
        EXAMPLE=example_data
    )

from app import views, models

