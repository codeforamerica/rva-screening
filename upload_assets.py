import flask_s3
from app import app

s3 = flask_s3.FlaskS3(app)

flask_s3.create_all(app)
