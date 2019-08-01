import base64
from flask_api import status
import io
import json
import unittest

from app.app import create_app, register_extensions
from app.config.config import TestingConfig
from app.models import models
from app.utils.extensions import db


class QuizCreation(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        register_extensions(self.app)
        # Create database tables
        with self.app.app_context():
            db.create_all()
        # Create client to test routes
        self.client = self.app.test_client()

    def test_quiz_create(self):
        # Read sample file
        sample_csv = open("tests/sample.csv", "rb").read()
        # Load file as bytes to be uploaded
        data = {"data": (io.BytesIO(sample_csv), "tests/sample.csv")}
        response = self.client.post('/quiz/create',
                                    content_type='multipart/form-data',
                                    data=data)
        with self.app.app_context():
            quiz = models.QA.query.filter_by(answer='England').first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json['message'], "Quiz created successfully")
        self.assertEqual(quiz.question, 'Chelsea is in what country?')

    def test_quiz_create_bad_file(self):
        # Read bad sample file
        bad_sample_csv = open("tests/bad_sample.csv", "rb").read()
        # Load file as bytes to be uploaded
        data = {"data": (io.BytesIO(bad_sample_csv), "tests/bad_sample.csv")}
        response = self.client.post('/quiz/create',
                                    content_type='multipart/form-data',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json['message'], "'Option C' column missing")

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class QuizView(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        register_extensions(self.app)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()
        self.create_quiz()

    def create_quiz(self):
        sample_csv = open("tests/sample.csv", "rb").read()
        data = {"data": (io.BytesIO(sample_csv), "tests/sample.csv")}
        self.client.post('/quiz/create',
                         content_type='multipart/form-data',
                         data=data)

    def test_view_unavailable_quiz(self):
        response = self.client.get("/quiz/2/view")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Page doesn't exist")

    def test_view_available_quiz(self):
        response = self.client.get("/quiz/1/view")
        options_a = ['Nigeria', 'Nigeria', 'Spain',
                     'Nigeria', 'Nigeria', 'Nigeria',
                     'Nigeria', 'Nigeria', 'Netherlands',
                     'Nigeria', 'Portugal', 'Nigeria', 'Nigeria']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["options_a"], options_a)

    def tearDown(self):
        with self.app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


class QuizSolve(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        register_extensions(self.app)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()
        credentials = base64.b64encode(b'Santa:AGift').decode('utf-8')
        self.headers = {'Authorization': 'Basic ' + credentials}
        self.register()
        self.create_quiz()

    def register(self):
        data = {'username': 'Santa',
                'password': 'AGift'}
        self.client.post(path='/user/register',
                         data=json.dumps(data),
                         content_type='application/json')

    def create_quiz(self):
        sample_csv = open("tests/sample.csv", "rb").read()
        data = {"data": (io.BytesIO(sample_csv), "tests/sample.csv")}
        self.client.post('/quiz/create',
                         content_type='multipart/form-data',
                         data=data)

    def test_solve_unavailable_quiz(self):
        data = {"answers": ["England", "England", "Spain", "Italy",
                            "Nigeria", "Scotland", "Germany", "Spain",
                            "Netherlands", "France", "Portugal", "Ghana",
                            "Swaziland"]}
        response = self.client.post("/quiz/2/solve",
                                    headers=self.headers,
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Page doesn't exist")

    def test_quiz_solve_with_credentials(self):
        data = {"answers": ["England", "England", "Spain", "Italy",
                            "Nigeria", "Scotland", "Germany", "Spain",
                            "Netherlands", "France", "Portugal", "Ghana",
                            "Swaziland"]}
        response = self.client.post("/quiz/1/solve",
                                    headers=self.headers,
                                    data=json.dumps(data),
                                    content_type='application/json')
        with self.app.app_context():
            score = models.Score.query.filter_by(id=1).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["message"], "Score is 93 percent")
        self.assertEqual(score.score, 93)

    def test_quiz_solve_without_credentials(self):
        data = {"answers": ["England", "England", "Spain", "Italy",
                            "Nigeria", "Scotland", "Germany", "Spain",
                            "Netherlands", "France", "Portugal", "Ghana",
                            "Sweden"]}
        response = self.client.post("/quiz/1/solve",
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_quiz_solve_with_invalid_number_of_answers(self):
        data = {"answers": ["England", "England", "Spain", "Italy",
                            "Nigeria", "Scotland", "Germany", "Spain",
                            "Netherlands", "France", "Portugal", "Ghana"]}
        response = self.client.post("/quiz/1/solve",
                                    headers=self.headers,
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json["message"],
                         "13 answers are not available")

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
