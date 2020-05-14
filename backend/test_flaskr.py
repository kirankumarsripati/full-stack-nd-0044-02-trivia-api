import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}"\
            .format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_categories(self):
        '''Get list of categories'''
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        '''Get list of questions'''
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_get_questions(self):
        '''Show error if invalid page number is provided'''
        res = self.client().get('/questions?page=9999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'questions not found')

    def missing_field_create_question(self, question, missing):
        '''Try to create a new question with a missing field'''
        missing_field_question = {}

        for key in question:
            if key != missing:
                missing_field_question[key] = question[key]

        res = self.client().post('/questions', json=missing_field_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], '{} cannot be blank'.format(missing))

    def test_create_question(self):
        '''Can create new question'''
        new_question = {
            'question': 'In which city is Jiddu Krishnamurti Foundation \
                School in Maharashtra?',
            'answer': 'Pune',
            'category': 3,
            'difficulty': 3
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_error_create_question(self):
        '''If any of the field is missing, throw error'''
        new_question = {
            'question': 'In which city is Jiddu Krishnamurti Foundation \
                School in Maharashtra?',
            'answer': 'Pune',
            'category': 3,
            'difficulty': 3
        }

        # case 1, question missing
        self.missing_field_create_question(
            question=new_question, missing='question')

        # case 2, answer missing
        self.missing_field_create_question(
            question=new_question, missing='answer')

        # case 3, category missing
        self.missing_field_create_question(
            question=new_question, missing='answer')

        # case 4, difficulty missing
        self.missing_field_create_question(
            question=new_question, missing='difficulty')

    def test_search_question(self):
        '''Search for question'''
        search_json = {
            'searchTerm': 'movie'
        }
        res = self.client().post('/questions', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_search_question_page(self):
        '''Fail to search for question with invalid page'''
        search_json = {
            'searchTerm': 'a',
            'page': 99999
        }
        res = self.client().post('/questions', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'no questions found with term - {}'.format(
                search_json['searchTerm']))

    def test_404_search_question(self):
        '''Fail to search for question with non existign term'''
        search_json = {
            'searchTerm': '~!@#$%^&*()_+'
        }
        res = self.client().post('/questions', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], 'no questions found with term - {}'.format(
                search_json['searchTerm']))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
