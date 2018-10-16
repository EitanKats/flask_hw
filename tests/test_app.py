import unittest

from app import app_factory


class MessagesTest(unittest.TestCase):
    def setUp(self):
        self.app = app_factory(config_name="testing")
        self.client = self.app.test_client
        self.message = {'name': 'i am a message'}

    def test_message_adding(self):
        res = self.client().post('/messages', data=self.message)
        print(res.data)
        self.assertEqual(201, res.status_code)
        self.assertIn('received', str(res.data))

    def test_api_when_there_are_no_messages(self):
        res = self.client().get('/messages')
        print(res.data)
        self.assertEqual(404, res.status_code)
        self.assertIn('no messages left', str(res.data))

    def test_message_adding(self):
        self.client().post('/messages', data=self.message)
        res = self.client().get('/messages')
        self.assertEqual(200, res.status_code)
        # self.assertIn('i am a message', str(res.data))


if __name__ == "__main__":
    unittest.main()
