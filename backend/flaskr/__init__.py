import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
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
         origins=['http://localhost:5173','http://127.0.0.1:5173'],
         supports_credentials=True   
         #allow_headers=['Content-Type','Authorization'] apenas se forem enviados esses headers no fetch.
    )

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
    
    @app.route('/addAllQuestions')
    def addQuestions():
        questions = [
            Question(question="Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", answer="Maya Angelou",              difficulty=2, category=4),
            Question(question="What boxer's original name is Cassius Clay?",                         answer="Muhammad Ali",              difficulty=1, category=4),
            Question(question="What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", answer="Apollo 13",        difficulty=4, category=5),
            Question(question="What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", answer="Tom Cruise", difficulty=4, category=5),
            Question(question="What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", answer="Edward Scissorhands", difficulty=3, category=5),
            Question(question="Which is the only team to play in every soccer World Cup tournament?", answer="Brazil",                   difficulty=3, category=6),
            Question(question="Which country won the first ever soccer World Cup in 1930?",           answer="Uruguay",                  difficulty=4, category=6),
            Question(question="Who invented Peanut Butter?",                                          answer="George Washington Carver",  difficulty=2, category=4),
            Question(question="What is the largest lake in Africa?",                                  answer="Lake Victoria",             difficulty=2, category=3),
            Question(question="In which royal palace would you find the Hall of Mirrors?",            answer="The Palace of Versailles",  difficulty=3, category=3),
            Question(question="The Taj Mahal is located in which Indian city?",                       answer="Agra",                      difficulty=2, category=3),
            Question(question="Which Dutch graphic artist–initials M C was a creator of optical illusions?", answer="Escher",          difficulty=1, category=2),
            Question(question="La Giaconda is better known as what?",                                 answer="Mona Lisa",                 difficulty=3, category=2),
            Question(question="How many paintings did Van Gogh sell in his lifetime?",                answer="One",                       difficulty=4, category=2),
            Question(question="Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?", answer="Jackson Pollock", difficulty=2, category=2),
            Question(question="What is the heaviest organ in the human body?",                        answer="The Liver",                 difficulty=4, category=1),
            Question(question="Who discovered penicillin?",                                           answer="Alexander Fleming",         difficulty=3, category=1),
            Question(question="Hematology is a branch of medicine involving the study of what?",      answer="Blood",                     difficulty=4, category=1),
            Question(question="Which dung beetle was worshipped by the ancient Egyptians?",           answer="Scarab",                    difficulty=4, category=4),
        ]

        for q in questions:
            q.insert()

        return 'Questions inserted!'

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
        stmt = db.select(Question).where(Question.category==id)
        rows = db.session.execute(stmt).scalars().all()
        #abortar quando não houver linhas
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
    @app.route('/questions/<int:id>',methods=['DELETE'])
    def delete_questions(id):
        try:
            print(f"O id recebido foi o {id}")
            question = db.session.get(Question,id)
            if not question:
                abort(404, description=f"O id: {id} não foi encontrado no db")
            question.delete()
            return {
                'success':True,
                'status':200,
                'deleted':f"{id}"
            }
        except Exception as e :
            print(str(e))
            abort(404, description=f'O id: {id} não existe')
            

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def post_questions():
        data = request.get_json()
        question = Question(
            question = data['question'],
            answer= data['answer'],
            difficulty= data['difficulty'],
            category= data['category']
        )
        question.insert()

        return {
            'success':True,
            'inserted': f"id : {question.id}"
        }

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
    done
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

    @app.errorhandler(500)
    def handle_500(err):
        return {
            'status':500,
            'success': False,
            'error': 'Internal Server Error',
            'message':getattr(err, 'description','')
        }, 500

    return app

if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True)