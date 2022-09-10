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
        self.database_path = "postgresql://{}/{}".format('postgres@localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"]) # making sure that there is some data that has "categories" as the key 
        self.assertTrue(len(data["categories"])) # making sure that there is some length to the data["categories"]


    # Test questions_pagination() for successful operation
    def test_questions_pagination(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    # Test questions_pagination() for expected errors
    def test_questions_pagination_failure(self):
        res = self.client().get("/questions>page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # Test delete_question() for successful execution 
    def test_delete_question(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test delete_question() for an expected error
    def test_delete_question_failure(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # Test add_search_question() for successful execution 
    def test_add_search_question(self):
        # test for adding question 
        question = {
        'question': "Test Question",
        'answer': "Test Answer" ,
        'category': "3",
        'difficulty': "4"
        }
        res = self.client().post("/questions", json = question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)


        # test for searching a question
        
        res = self.client().post("/questions", json = {'searchTerm' :'the'})
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    # Test add_search_question() for expected failure
    def test_add_search_question_failure(self):
        # test for adding question 
        question = {
        'question': "Test Question",
        'answer': "Test Answer" ,
        'difficulty': "4"
        }
        res = self.client().post("/questions", json = question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # Test search_category_for_question() for successful execution 
    def test_category_for_question(self):
        res = self.client().get("/categories/3/questions")
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        

    # Test search_category_for_question() for expected error 
    def test_category_for_question_failure(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # Test play_quiz() for succesful execution 
    def test_play_quiz(self):
        res = self.client().post("/quizzes", json = {'previous_questions': [], 'quiz_category': {'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))


    # Test play_quiz() for expected error 
    def test_play_quiz_failure(self):
        res = self.client().post("/quizzes", json = {'previous_questions': [], 'quiz_category': {'id':8}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()