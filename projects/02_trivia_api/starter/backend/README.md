# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous questions parameters and return a random question within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Documentation

The trivia-API functions as a backend for the trivia-frontend. It offers endpoints to get available questions (also per category), add new questions and deliver random questions for the game. 

### Datatypes and Errors

The API consumes and returns JSON-Objects. Status code for successful API-Requests is always _200_. Every answer object includes a _success_ attribute with the value _True_ if the request can be responed successful and the value _False_ in case of an error.

Error Objects have the following structure:
```
{
    'success': False,
    'error': <status-code, for example 404>,
    'message': '<errormsg, for example _file not found_>'
}

```

Expectable Errors:
| Status Code | Error message | Explanation|
| --- | --- | --- |
| 400 | information missing | a required parameter was not supplied |
| 404 | resource not found | the resource you requested is not available, for example a non existing endpoint, a non existing question or a page out of bound |
| 405 | method not allowed | the method (GET, POST, PUT, PATCH, DELETE) you used is not supported by the endpoint |
| 422 | not processable | the request could not be processed  |
| 500 | internal server error | an error on server side prevented the response to the request|

### Authentification
The API requires no autentification.

### API-Endpoints for Questions

#### GET /questions - get paginated questions

This endpoint returns a list of available questions, paginated by 10 together with available categories. The query parameter 'page' controls the pagination and helps to go to futher pages.

- Query-Parameter _page_ (Type int, default 1): controls the pagination. page=1 returns the first 10 questions, page=2 the questions 11-20, etc.
- Request Parameter: none
- Response: JSON-Object with the attributes:
  - _categories_: a list of categories
  - _current_category_: null
  - _questions_: a list of questions objects with the attributes  _id_, a _question_, an _answer_, a _difficulty_ and a _category_
  - _total_question_: the total number of questions in this category 
  - _success_: boolean 

Example request:
```

curl http://localhost:5000/questions?page=2

```

Example response:
```

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Lilly and Goldi",
      "category": 5,
      "difficulty": 1,
      "id": 1,
      "question": "Who are the best pets in town?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "-b +- sqr(b2-4ac) / 2a",
      "category": 5,
      "difficulty": 3,
      "id": 3,
      "question": "What is the midnight formula?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 18




```

#### POST /questions 

##### Add a new question
To add a new question you can post all required information (question, answer, difficulty and category) in form of a JSON-Object to the /questions endpoint.

- Request parameter: JSON-Object with the attributes
  - _question_: <your question text>, string
  - _answer_: <your answer text>, string
  - _difficulty_: integer between 1 (very easy) to 5 (very hard)
  - _category_: id of the category of the question, integer 
- Response: JSON-Object with the attributes _created_ with the id of the newly created question and _success_ = True
- Expectable errors: 
  - 400 (missing information): if the request misses some of the required information
  - 422 (unprocessable): request resulted in a database error

Example request:
```

curl -X POST http://localhost:5000/questions -d '{"question":"A very hard question?", "answer": "The amazing answer", "difficulty" : 5, "category": 1}' -H 'Content-Type: application/json'

```

Example response:
```
{
  "created": 5,
  "success": true
}


```
##### Search for questions

To search for questions, post the search-term to the /questions endpoint, resulting in a list of all questions that entail the search term in their question or answer, paginated by 10 questions. Search is insensitive.

- Request parameter: JSON-Object with the attribute _searchTerm_ as a string
- Query parameter: _page_ to control pagination, see above at GET /questions
- Response: JSON-Object with the attributes:
  - _categories_: a list of categories
  - _current_category_: null
  - _questions_: a list of questions objects with the attributes  _id_, a _question_, an _answer_, a _difficulty_ and a _category_
  - _total_question_: the total number of questions found 
  - _success_: boolean

Example request:
```
curl -X POST http://localhost:5000/questions?page=1 -d '{"searchTerm":"actor"}' -H 'Content-Type: application/json'
```

Example response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "total_questions": 1
}

```

#### DELETE /questions/<int:id>
To delete a question, send a DELETE request with the id of the question as a path-parameter. The question is deleted without further warning and returns the deleted question ID.
- Path parameter: id (int), identifier of the question to be deleted
- Response: JSON-Object with the attributes _deleted_ and _success_
- Expectable errors: 
  - 404 (resource not found): if there is no question with the provided id
  - 422 (unprocessable): request resulted in a database error

Example request:
```
curl -X DELETE http://localhost:5000/questions/1
```

Example response:
```
{
  "deleted": 1,
  "success": true
}

```


### Categories

#### GET /categories
This endpoint returns a dictionary of all available categories.

- Request/path/query parameters: None
- Response: JSON object with the attributes 
  - _success_ as a boolean with True for success and False for an error and 
  - _categories_ as a dictionary in which the keys are the ids and the values are the corresponding name of the category.


Example request:
```
curl http://localhost:5000/categories
```

Example response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```


#### GET /categories/<int: cat_id>/questions

This endpoint return the questions of a specific category paginated by 10 questions.

- Path parameter cat_id (integer): ID of the category
- Query parameter _page_ (integer): controls pagination, see above at GET /questions
- Response: JSON-Object with the attributes:
  - _categories_: a list of categories
  - _current_category_: the id of the current category
  - _questions_: a list of questions objects with the attributes  _id_, a _question_, an _answer_, a _difficulty_ and a _category_
  - _total_question_: the total number of questions in this category 
  - _success_: boolean 
- Expectable errors:
  - 404 (resource not found), if the number of questions is 0 or the page requested is out of bounds.

Example request:
```
curl http://localhost:5000/categories/1/questions?page=1
```

Example response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 1,
  "questions": [
    {
      "answer": "The amazing answer",
      "category": 1,
      "difficulty": 5,
      "id": 5,
      "question": "A very hard question?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 4
}

```
### Quizzes

A quiz is sequence of queries from one category or mixed from all categories. 

#### POST /quizzes

This endpoint delivers the next random question of a quiz in the demanded category that was not posed before in the quiz. The quiz is defined by the id of the category of questions and a list of previous questions.
- Request parameter: JSON object with attributes
  - _quiz_category_: Demanded category as a dict with attributes _id_ (integer) and _type_ (string). Choose _id_ = 0 for all categories
  - _previous_questions_: List of previous question ids already posed in this quiz. Empty list at the beginning of the quiz
- Response: JSON object including the next question and a success marker
  - _question_: next question in quiz as a JSON object with attributes _id_ (int) _question_ (string), _answer_ (string), _category_ (int id of catgory) and _difficulty_ (int between 1 (very easy) and 5 (very hard)). This attribute is missing when there is no question left for the quiz.
  - _success_: boolean with True for successful requests and False for errors
- Expectable errors:
  - 400 (missing information): if the request data misses required information (_quiz_category_ and _previous_questions_) 

Example request:
```
curl -X POST http://localhost:5000/quizzes -d '{"quiz_category":{"id":1,"type":"Science"}, "previous_questions":[20,5]}' -H 'Content-Type: application/json'

```

Example response:
```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```