import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import choice

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)


    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources = {r'/api/*': {'origins': "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()

        dict_of_categories = { str(category.id) : category.type for category in categories }

        return jsonify({ "success": True, "categories" : dict_of_categories })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def questions_pagination():  
        page_number = request.args.get('page', 1, type = int)
        questions = Question.query.order_by(Question.id).all()
        start = (page_number - 1) * QUESTIONS_PER_PAGE
        end = page_number * QUESTIONS_PER_PAGE

        paginated_questions = [question.format() for question in questions][start:end]
        if (len(paginated_questions)==0):
            abort(404)
        else:
            return jsonify({ "success": True, 
                "questions": paginated_questions, 
                "total_questions": len(questions), 
                "categories": {category.id : category.type for category in Category.query.all()}, 
                "current_category": ""})
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:id_to_delete>", methods = ["DELETE"])
    def delete_question(id_to_delete):
        question = Question.query.filter_by(id = id_to_delete).one_or_none()

        if question is None:
            abort(422)
        else:
            question.delete()
            return jsonify({
                "success": True
                })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # the route and method for searching and addding a new question is the same.
    @app.route("/questions", methods = ['POST'])
    def add_search_question():
        data = request.get_json()

        if ('searchTerm' in data):
            searchTerm = data.get('searchTerm')
            
            try:
                questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
                return jsonify({
                    "success": True,
                    "questions": [ question.format() for question in questions],
                    "total_questions": len(questions),
                    "current_category": " "
                    })
            except:
                abort(422)
        elif ('question' not in data or 'answer' not in data or 'category' not in data or 'difficulty' not in data):
            abort(422)
        else:
            try:
                question_sent = data.get('question')
                answer_sent = data.get('answer')
                category_sent = data.get('category')
                difficulty_sent = data.get('difficulty')
                question = Question(question = question_sent, answer = answer_sent, category = category_sent, difficulty = difficulty_sent)
                question.insert()

                return jsonify({
                    "success": True
                    })
            except:
                abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_to_search>/questions", methods= ['GET'])
    def search_category_for_question(category_to_search):
        questions = Question.query.filter_by(category = category_to_search).all()

        if len(questions) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": str(category_to_search)
                })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods = ['POST'])
    def play_quiz():
        body = request.get_json()
        previous = body.get("previous_questions", None)
        category = body.get("quiz_category")
        
        if category['id'] is not 0:
            questions = Question.query.filter_by(category = category['id']).filter(~Question.id.in_(previous)).all()
        else:
            questions = Question.query.filter(~Question.id.in_(previous)).all()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "question": choice(questions).format()
            })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # Used only 404 and 422 
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not Found",
            "error": 404
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "message": "Request unprocessable",
            "error": 422
            }), 422

    return app