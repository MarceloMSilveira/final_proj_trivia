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

    #before requests:
    @app.before_request
    def _dbg():
        print('>>', request.method, request.path, request.query_string)
        #print('URL map:')
        #print(app.url_map)

    #aux functions
    def paginate(questions,page):
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return [q for q in questions[start:end]]

    @app.route('/')
    def hello_home():
        row = db.session.execute(db.select(Question)).scalars().first()
        q = row.question
        return f'ok: {q}'
    
    """
    @TODO:
    done
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def all_categories():
        rows = db.session.execute(db.select(Category).order_by(Category.id)).scalars().all()
        categories = {r.id:r.type for r in rows}
        return {
            'success':True,
            'categories':categories,
            'total':len(categories)
        }

    """
    @TODO:
    done
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page',1,type=int)
        stmt = db.select(Question).order_by(Question.id)
        rows = db.session.execute(stmt).scalars().all()
        rows_categories = db.session.execute(db.select(Category)).scalars().all()
        categories = {r.id : r.type for r in rows_categories}

        questions = [{'id':q.id,
                      'question':q.question,
                      'answer':q.answer,
                      'category':q.category,
                      'difficulty':q.difficulty
                      } for q in rows]
    
        total = len(questions)
        paginate_questions = paginate(questions,page)
        if len(paginate_questions)==0:
            abort(400, description= f"A pagina nr {page} não existe")
        return {
            "success":True,
            "questions":paginate_questions,
            "total_questions": total,
            "categories":categories,
            "current_category":1
        }

    """
        @TODO:
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def question_by_category(id):
        categories_id = [1,2,3,4,5,6]
        if id not in categories_id:
            abort(404, description=f"A categoria {id} não existe")
        stmt = db.select(Question.question).where(Question.category==id)
        rows = db.session.execute(stmt).scalars().all()
        
        questions = [{'id':q.id,
                      'question':q.question,
                      'answer':q.answer,
                      'category':q.category,
                      'difficulty':q.difficulty
                      } for q in rows]

        return {
            'success':True,
            'questions':questions,
            'total_questions':len(questions),
            'current_category':id
        }
        
    

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

    @app.errorhandler(400)
    def handle_400(err):
        return {
            'status':400,
            'success': False,
            'error': 'bad request',
            'message':getattr(err, 'description','')
        }, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {
            'status':404,
            'success': False,
            'error': 'resource not found',
            'message':getattr(err, 'description','')
        }, 404

    @app.errorhandler(405)
    def handle_405(err):
        return {
            'status':405,
            'success': False,
            'error': 'Method not allowed',
            'message':getattr(err, 'description','')
        }, 405
    
    @app.errorhandler(415)
    def unsupported_type(error):
        return{
            "status": 415,
            "success":False,
            "error": 'unsupported type',
            "message":getattr(error, 'description','')
        }, 415
    
    @app.errorhandler(422)
    def handle_422(err):
        return {
            'status':422,
            'success': False,
            'error': 'Unprocessable Entity',
            'message':getattr(err, 'description','')
        }, 422

    return app

if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True)