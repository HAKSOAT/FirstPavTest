from flask_api import status
import json
import unittest

from app.app import create_app, register_extensions
from app.utils.extensions import db
from app.config.config import TestingConfig
from app.models import models


class UserRegistration(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        register_extensions(self.app)
        # Create database tables
        with self.app.app_context():
            db.create_all()
        # Create client to test routes
        self.client = self.app.test_client()

    def test_user_register_right_parameters(self):
        data = {'username': 'Santa',
                'password': 'AGift'}
        response = self.client.post(path='/user/register',
                                    data=json.dumps(data),
                                    content_type='application/json')
        with self.app.app_context():
            user = models.User.query.filter_by(username='Santa'.lower()).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json['message'],
                         "Account created successfully")
        self.assertNotEqual(user, None)

    def test_user_register_wrong_parameters(self):
        data = {'usernames': 'Santa',
                'password': 'AGift'}
        response = self.client.post(path='/user/register',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json['message'], "'username' not found")

    def test_user_register_twice(self):
        data = {'username': 'Santa',
                'password': 'AGift'}
        self.client.post(path='/user/register',
                         data=json.dumps(data),
                         content_type='application/json')
        response = self.client.post(path='/user/register',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json['message'], "Account already exists")

    def tearDown(self):
        with self.app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
