from tests.unit.test_base import BaseTestCase

class TestScreener(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

