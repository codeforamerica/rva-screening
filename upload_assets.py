import flask_s3
import logging
from app import create_app

# For Aptible
logging.basicConfig()

app = create_app()

s3 = flask_s3.FlaskS3(app)

flask_s3.create_all(app)
