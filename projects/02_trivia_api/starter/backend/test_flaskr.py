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
        self.database_path = "postgres://{}:{}@{}/{}".format('diglezakis','di1TPfDI!','localhost:5432', self.database_name)
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
    
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = response.json
        self.assertEqual(response.status_code,200)
        self.assertTrue(data.get('success'))

        cats = response.json.get('categories')
        cids = sorted([int(key) for key in cats.keys()]) #[cat['id'] for cat in cats]
        dbCats = Category.query.all()
        dbids = sorted([c.id for c in dbCats])
        self.assertEqual(cids,dbids)

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = response.json
        self.assertEqual(response.status_code,200)
        self.assertTrue(data.get('success'))
        self.assertEqual(len(data.get('questions')),10)
        qids = [q["id"] for q in data.get('questions')]
        self.assertEqual(qids,sorted([q.id for q in Question.query.order_by(Question.id).all()[0:10]]))

    def test_get_questions_from_second_page(self):
        response = self.client().get('/questions?page=2')
        data = response.json
        self.assertEqual(response.status_code,200)
        self.assertTrue(data.get('success'))
        qids = [q["id"] for q in data.get('questions')]
        self.assertEqual(qids,sorted([q.id for q in Question.query.order_by(Question.id).all()[10:]]))

    def test_get_questions_out_of_range(self):
        response = self.client().get('/questions?page=999')
        data = response.json
        self.assertEqual(response.status_code,404)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get("error"),404)
        self.assertEqual(data.get("message"),"resource not found")

        
    def test_delete_question(self):
        qid = Question.query.all()[0].id
        response = self.client().delete('/questions/{}'.format(qid))
        data = response.json
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code,200)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('deleted'),qid)
        self.assertIsNone(Question.query.get(qid))

    def test_delete_non_existing_query(self):
        qid = 99999
        response = self.client().delete('/questions/{}'.format(qid))
        data = response.json
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data.get("error"),404)
        self.assertEqual(data.get("message"),"resource not found")
        self.assertFalse(data.get("success"))


    def test_create_new_question(self):
        new_question = {
            'question': 'Who are the best pets in town?',
            'answer': 'Lilly and Goldi',
            'difficulty': 2,
            'category' : 2}
        num1 = len(Question.query.all())
        response = self.client().post('/questions',json=new_question)
        data = response.json
        cid = data.get('created')
        self.assertEqual(response.status_code,200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(Question.query.get(int(cid)))
        self.assertEqual(num1+1,len(Question.query.all()))

    def test_create_question_without_enough_information(self):
        question_wo_question = {
            'answer': 'Lilly and Goldi',
            'difficulty': 2,
            'category' : 2}

        question_wo_answer = {
            'question': 'Who are the best pets in town?',
            'difficulty': 2,
            'category' : 2}
        question_wo_difficulty = {
            'question': 'Who are the best pets in town?',
            'answer': 'Lilly and Goldi',
            'category' : 2}
        question_wo_category = {
            'question': 'Who are the best pets in town?',
            'answer': 'Lilly and Goldi',
            'difficulty': 2}
 
        response = self.client().post('/questions',json=question_wo_question)
        data = response.json
        self.assertEqual(response.status_code,400)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'),400)
        self.assertEqual(data.get('message'),'information missing')

        response = self.client().post('/questions',json=question_wo_answer)
        data = response.json
        self.assertEqual(response.status_code,400)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'),400)
        self.assertEqual(data.get('message'),'information missing')

        response = self.client().post('/questions',json=question_wo_difficulty)
        data = response.json
        self.assertEqual(response.status_code,400)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'),400)
        self.assertEqual(data.get('message'),'information missing')

        response = self.client().post('/questions',json=question_wo_category)
        data = response.json
        self.assertEqual(response.status_code,400)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'),400)
        self.assertEqual(data.get('message'),'information missing')
    
    def test_search_questions(self):
        search = 'actor'
        response = self.client().post('/questions',json={'searchTerm':search})
        data = response.json
        self.assertEqual(response.status_code,200)
        questions = data.get('questions')
        self.assertIsNotNone(questions)
        for q in questions:
            self.assertTrue(str(q['question']).find(search) != -1 or str(q['answer']).find(search) != -1)

    def test_get_questions_of_category(self):
        cat_id = 2
        response = self.client().get('/categories/{}/questions'.format(cat_id))
        data = response.json
        self.assertEqual(response.status_code,200)
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('current_category'),cat_id)
        questions = data.get('questions')
        for q in questions:
            self.assertEqual(int(q['category']),cat_id)

    def test_get_category_questions_out_of_bound(self):
        cat_id = 2
        response = self.client().get('/categories/{}/questions?page=999'.format(cat_id))
        data = response.json
        self.assertEqual(response.status_code,404)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'),404)

    def test_quizz(self):
        category = {'id':2, 'type': 'Science'}
        previous_questions = []
        next_question = True
        while(next_question):
            response = self.client().post('/quizzes',
            json={'previous_questions':previous_questions,'quiz_category':category})
            self.assertEqual(response.status_code,200)
            next_question = response.json.get('question') is not None
            if next_question:
                self.assertNotIn(response.json.get('question')['id'],previous_questions)
                previous_questions.append(response.json.get('question')['id'])
        
        

#    """
#    TODO
#    Write at least one test for each test for successful operation and for expected errors.
#    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()