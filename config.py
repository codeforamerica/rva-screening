import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/rva_screening')
