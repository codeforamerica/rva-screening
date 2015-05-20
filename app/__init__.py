import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from werkzeug import secure_filename
from config import Config

app = Flask(__name__, static_url_path='')

app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
# unless we are in a production environment, turn on debug
app.debug = app.config['SCREENER_ENVIRONMENT'] != 'prod'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.context_processor
def inject_static_url():
    """Adds `STATIC_URL` variable to template context.
    """
    static_url = os.environ.get('STATIC_URL', app.static_url_path)
    if not static_url.endswith('/'):
        static_url += '/'
    return dict(
        static_url=static_url
    )

@app.context_processor
def inject_example_data():
    """Adds `EXAMPLE` variable to template context, if we need to fake data
    somewhere.
    """
    from app import example_data
    return dict(EXAMPLE=example_data)


from app import views, models

