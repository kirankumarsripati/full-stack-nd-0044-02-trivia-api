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

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
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
        self.assertEqual(data['error'], 404)
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
        self.assertEqual(data['error'], 404)
        self.assertEqual(
            data['message'], 'no questions found with term - {}'.format(
                search_json['searchTerm']))

    def test_delete_question(self):
        '''Delete a question'''
        # To work in any case, first add a question
        new_question = {
            'question': 'In which city is Jiddu Krishnamurti Foundation \
                School in Maharashtra?',
            'answer': 'Pune',
            'category': 3,
            'difficulty': 3
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        # store added question id
        question_id = data['created']

        # delete added question
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_404_delete_question(self):
        '''Delete a non existing question id'''
        res = self.client().delete('/questions/9999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'question not found')

    def test_get_questions_by_category(self):
        '''Get questions by category'''
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'], 1)

    def test_404_catgory_get_questions_by_category(self):
        '''Get questions by invalid category'''
        res = self.client().get('/categories/9999999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'category not found')

    def test_404_question_get_questions_by_category(self):
        '''Get questions by invalid page'''
        res = self.client().get('/categories/1/questions?page=9999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'questions not found')

    def test_get_quiz_all(self):
        '''Get quiz for all category'''
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['question'])

    def test_get_quiz_with_category(self):
        '''Get quiz for specific category'''
        quiz_info = {
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        res = self.client().post('/quizzes', json=quiz_info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['question'])

    def test_get_quiz_with_category_prev_questions(self):
        '''Get quiz for specific category and previous questions'''
        quiz_info = {
            'previous_questions': [20],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        res = self.client().post('/quizzes', json=quiz_info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question']['id']
                        not in quiz_info['previous_questions'])
        self.assertTrue(data['question']['category'],
                        quiz_info['quiz_category']['id'])

    def test_405_get_quiz(self):
        '''Get quizzes with GET method'''
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
