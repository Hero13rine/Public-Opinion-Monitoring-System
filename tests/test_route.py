import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_evaluate(self):
        response = self.app.post('/evaluate', json={"text": "测试微博内容"})
        self.assertEqual(response.status_code, 200)
