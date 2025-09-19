import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from config_db import db
from models import Question, Category
from flask_migrate import Migrate

QUESTIONS_PER_PAGE = 10

migrate = Migrate()

def create_app(config_object='config'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)

    migrate.init_app(app,db)

    with app.app_context():
        db.create_all()

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app,
         origins=['http://localhost:5173'],
         methods=['GET','POST'],
         supports_credentials=True   
         )
    
    #CASO NECESSÁRIO EM ALGUMA ROTA EM ESPECIAL USAR
    #@cross_origin()

    @app.route('/')
    def hello_home():
        row = db.session.execute(db.select(Question)).scalars().first()
        q = row.question
        return f'ok: {q}'
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def all_categories():
        rows = db.session.execute(db.select(Category).order_by(Category.id)).scalars().all()
        categories = [r.type for r in rows]
        return {
            'success':True,
            'categories':categories,
            'total':len(categories)
        }

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

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(405)
    def handle_405(err):
        return {
            'success': False,
            'error': 405,
            'message':'Method Not Allowed'
        }, 405

    return app

if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True)