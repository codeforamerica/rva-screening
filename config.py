import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/rva_screening')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
