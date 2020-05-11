import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_results(selection,request):
  """
    Helper function supplies pagination of questions:
    - selection: list of questions
    - request: flask request including query parameter 'page' as int
  """
  page = request.args.get('page',1,int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = min(len(selection),start + QUESTIONS_PER_PAGE)
  return selection[start:end]



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app, origins='*')
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  @app.after_request
  def after_request(response):
    """
    Sets up CORS headers for all requests
    """  
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return response
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.route('/categories')
  def get_categories():
    """
    Returns all available categories as a dictionary with keys as category id and values the corresponding category type 
    """
    cats = Category.query.all()
    resp = {
      'success' : True,
      'categories' : {cat.id: cat.type for cat in cats}
    }
    return jsonify(resp)

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/questions')
  def get_questions():
    """
    Returns all available questions paginated as 10 questions 
    """
    
    all_questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_results(all_questions,request)
    if len(current_questions) == 0:
      abort(404)

    resp= {
      'success': True,
      'questions': [q.format() for q in current_questions],
      'total_questions': len(all_questions),
      'categories': {cat.id: cat.type for cat in Category.query.all()},
      'current_category': None
    }
    return jsonify(resp)
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''


  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  def delete_question(question_id):
    """
    Deletes a question identified by question_id as int 
    """

    question = Question.query.get(question_id)
    if question is None:
      abort(404)
    else:
      try:
        question.delete()
        response = {
          'success':True,
          'deleted':question.id}
      except:
        abort(422)
    return jsonify(response)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions',methods=["POST"])
  def create_or_search_question():
    """
     creates a new question (with attributes question, answer, difficulty and category) 
     or searches for questions with searchTerm in question or answer
    """

    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    difficulty = data.get('difficulty')
    category = data.get('category')
    search = data.get('searchTerm')

    if search is not None:
      all_questions = Question.query.order_by(Question.id).filter(or_(Question.answer.ilike('%{}%'.format(search)),Question.question.ilike('%{}%'.format(search)))).all()
      current_questions = paginate_results(all_questions,request)

      response= {
        'success': True,
        'questions': [q.format() for q in current_questions],
        'total_questions': len(all_questions),
        'categories': {cat.id: cat.type for cat in Category.query.all()},
        'current_category': None
      }
 

    elif question is None or answer is None or difficulty is None or category is None:
      abort(400) 
    else:
      question = Question(question=question, answer=answer, difficulty=difficulty, category=category)

      try:
        question.insert()
        response = {
          'success': True,
          'created': question.id
         }
      except:
        abort(422)
    return jsonify(response)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/categories/<int:cat_id>/questions')
  def get_questions_of_category(cat_id):
    """
    Returns all available questions of a category identified by id cat_id, paginated by 10 questions 
    """

    all_questions = Question.query.order_by(Question.id).filter(Question.category==cat_id).all()
    current_questions = paginate_results(all_questions,request)
    if len(current_questions) == 0:
      abort(404)

    resp= {
      'success': True,
      'questions': [q.format() for q in current_questions],
      'total_questions': len(all_questions),
      'categories': {cat.id: cat.type for cat in Category.query.all()},
      'current_category': cat_id
    }
    return jsonify(resp)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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
  @app.route('/quizzes', methods=["POST"])
  def get_quiz_question():
    """
    Returns the next random question of a quiz from a specific category (defined by dict quiz_category) 
    that was not posed in this quiz before (defined by list previous_questions)  
    """

    data = request.json
    prev_questions = data.get('previous_questions')
    category = data.get('quiz_category')
    if prev_questions is None or category is None:
      abort(400)
    else:
      cid = category['id']
      if cid != 0 and len(prev_questions) > 0:
        questions = Question.query.filter(
          and_(
            Question.category==cid,
            Question.id.notin_(prev_questions)
          )
        ).all()
      elif cid != 0 and len(prev_questions) == 0:
        questions = Question.query.filter(Question.category==cid).all()
      elif cid == 0 and len(prev_questions) != 0:
        questions = Question.query.filter(Question.id.notin_(prev_questions)).all()
      else:
        questions = Question.query.all()
      random.seed()
      if len(questions) > 0:
        question = random.choice(questions)
        response = {
        'success': True,
        'question': question.format()
        }
      else:
        response = {
        'success': True,
        }
      
    return jsonify(response)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found_404(error):
    """
    Errorhandler for 404 (ressource not found) error
    """

    response = jsonify({'success': False,
                'error': 404,
                'message': 'resource not found'}), 404
    return response 

  @app.errorhandler(405)
  def not_found_405(error):
    """
    Errorhandler for 405 (method not allowed) error
    """
    response = jsonify({'success': False,
                'error': 405,
                'message': 'method not allowed'}), 405
    return response  

  @app.errorhandler(422)
  def not_proccessable_422(error):
    """
    Errorhandler for 422 (request not proccessable) error
    """
    response = jsonify({
      'success': False,
      'error': 422,
      'message': 'request not processable'})

  @app.errorhandler(400)
  def bad_request_400(error):
    """
    Errorhandler for 400 (bad request) error, 
    used in this API for missing information in the request
    """
    response = jsonify({'success': False,
                'error': 400,
                'message': 'information missing'}), 400
    return response 

  @app.errorhandler(500)
  def internal_server_error_500(error):
    response = jsonify({'success': False,
                'error': 500,
                'message': 'internal server error'}), 500
    return response 

  return app

    