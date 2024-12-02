import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_sum(self):
        payload = {'num1': 2, 'num2': 3}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 5)

    def test_negative_sum(self):
        payload = {'num1':5, 'num2':-7}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], -2)

if __name__ == "__main__":
    unittest.main()