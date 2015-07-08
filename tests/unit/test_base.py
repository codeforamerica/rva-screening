from app import create_app as _create_app
from app import db
from config import TestConfig
from flask_testing import TestCase

class BaseTestCase(TestCase):

    def create_app(self):
        return _create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()

