import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/rva_screening')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
IS_PRODUCTION = os.environ.get('IS_PRODUCTION', False)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = 'rva-screener'
S3_ONLY_MODIFIED = False
