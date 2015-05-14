import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/rva_screening')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
SCREENER_ENVIRONMENT = os.environ.get('SCREENER_ENVIRONMENT')
S3_BUCKET_NAME = 'rva-screener'
S3_ONLY_MODIFIED = False
