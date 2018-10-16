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
        self.assertEqual(res.status_code, 201)
        self.assertIn('received', str(res.data))

    def test_api_when_there_are_no_messages(self):
        res = self.client().get('/messages')
        print(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertIn('no messages left', str(res.data))

    def test_message_adding(self):
        self.client().post('/messages', data=self.message)
        res = self.client().get('/messages')
        self.assertEqual(res.status_code, 200)
        # self.assertIn('i am a message', str(res.data))


if __name__ == "__main__":
    unittest.main()
