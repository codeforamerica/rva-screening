import flask_s3
from app import create_app

app = create_app()

s3 = flask_s3.FlaskS3(app)

flask_s3.create_all(app)
