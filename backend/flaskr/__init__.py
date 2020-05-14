import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    DONE: Set up CORS. Allow '*' for origins.
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''Returns a list of categories dict'''
    def get_categories_json():
        categories = Category.query.all()
        if not categories:
            abort(404, description={'message': 'no category found'})

        return [category.format() for category in categories]

    '''
    DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        '''Returns all the categories.'''

        categories_json = get_categories_json()

        return jsonify({
            'success': True,
            'categories': categories_json
        })

    '''
    DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the
    screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        selection = Question.query.order_by(Question.id).paginate(
            page,
            QUESTIONS_PER_PAGE,
            False)
        current_questions = [question.format() for question in selection.items]

        if len(current_questions) == 0:
            abort(404, {'message': 'questions not found'})

        categories_json = get_categories_json()

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': selection.total,
            'categories': categories_json,
            'current_category': None
        })

    '''
    DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the
    question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404, {'message': 'question not found'})

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })
        except OperationalError:
            abort(422)

    '''
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of
    the last page of the questions list in the "List" tab.

    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        '''
        Handle 2 cases
        1. Create new question
        2. Search questions
        '''
        body = request.get_json()

        if not body:
            abort(400, {'message': 'invalid body JSON'})

        search_term = body.get('searchTerm', None)

        if search_term:
            page = body.get('page', 1)
            # search for the term in the question
            search_questions = Question.query.filter(Question.question.ilike(
                '%' + search_term + '%')).paginate(
                    page,
                    QUESTIONS_PER_PAGE,
                    False)

            questions_json = [question.format()
                              for question in search_questions.items]

            if len(questions_json) == 0:
                abort(404, {'message': 'no questions found with term - {}'.format(
                    search_term)})

            return jsonify({
                'success': True,
                'questions': questions_json,
                'total_questions': search_questions.total,
                'current_category': None
            })

        # if not search term, then create question
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if not new_question:
            abort(400, {'message': '{} cannot be blank'.format('question')})

        if not new_answer:
            abort(400, {'message': '{} cannot be blank'.format('answer')})

        if not new_category:
            abort(400, {'message': '{} cannot be blank'.format('category')})

        if not new_difficulty:
            abort(400, {'message': '{} cannot be blank'.format('difficulty')})

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })
        except OperationalError:
            abort(422)

    '''
    DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        current_category = Category.\
            query.filter(Category.id == category_id).one_or_none()

        if not current_category:
            abort(404, {'message': 'category not found'})

        page = request.args.get('page', 1, type=int)
        selection = Question.query.\
            filter(Question.category == category_id).\
            order_by(Question.id).\
            paginate(
                page,
                QUESTIONS_PER_PAGE,
                False)
        current_questions = [question.format() for question in selection.items]

        if len(current_questions) == 0:
            abort(404, {'message': 'questions not found'})

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': selection.total,
            'current_category': category_id
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': get_error_message(error, 'bad request')
        }), 400

    '''
    DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': get_error_message(error, 'resource not found')
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': get_error_message(error, 'unprocessable entity')
        }), 422

    def get_error_message(error, default_message):
        '''
        Returns if there is any error message provided in
        error.description.message else default_message
        This can be passed by calling
        abort(404, description={'message': 'your message'})

        Parameters:
        error (werkzeug.exceptions.NotFound): error object
        default_message (str): default message if custom message not available

        Returns:
        str: Custom error message or default error message
        '''
        try:
            return error.description['message']
        except TypeError:
            return default_message

    return app
