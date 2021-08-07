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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'pupu0819', 'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_categories(self):
        """ Test getting all paginated categories. """
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('success')
        self.assertTrue(data['categories'])

    def test_404_get_categories_beyond_valid_page(self):
        """ Test getting categories with invalid page. """
        response = self.client().get('/categories?page=100')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not Found")

    def test_get_paginated_questions(self):
        """ Test getting all paginated questions. """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_get_question_beyond_valid_page(self):
        """ Test getting questions with invalid page. """
        response = self.client().get('/question?page=100')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not Found")

    def test_get_questions_by_category(self):
        """ Test getting paginated questions based on the given category. """
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_get_questions_by_inexistent_category(self):
        """ Test failed getting paginated questions based on category
            which does not exist.
        """
        response = self.client().get('/categories/1000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not Found")

    def test_delete_question(self):
        """ Test deleting the specific question. """
        before_delete = len(Question.query.all())
        response = self.client().delete('questions/31')
        after_delete = len(Question.query.all())
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(before_delete, after_delete + 1)

    def test_404_failed_delete(self):
        """ Test deleting an inexistent question. """
        response = self.client().delete('questions/24')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_get_next_quiz(self):
        """ Test getting the next quiz. """
        request_json = {
            'previous_questions': [5, 9, 12],
            'quiz_category': {'id': 4}
        }
        response = self.client().post('/quizzes', json=request_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_405_not_allowed_next_quiz(self):
        """ Test getting the next quiz without request body. """
        response = self.client().get('/quizzes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Not Allowed Method")

    def test_400_failed_get_next_quiz(self):
        """ Test getting the next quiz without request body. """
        response = self.client().post('/quizzes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad Request")

    def test_create_new_question(self):
        """ Test creating a new question. """
        new_question = {
            'question': "What color is the sun?",
            'answer': "It’s a mixture of all colors.",
            'category': "1",
            'difficulty': 2
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_failed_creation(self):
        """ Test failing in creating new question with bad request. """
        response = self.client().post('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    def test_search_questions(self):
        """ Test searching for questions. """
        search_item = {
            'searchTerm': 'sun'
        }
        response = self.client().post('/questions', json=search_item)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['totalQuestions'], 2)

    def test_failed_search(self):
        """ Test failing in searching question with inexistent string. """
        response = self.client().post('/questions', json={'searchTerm': 'abcdef'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 0)
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
