import unittest
import json

from config_db import db
from flaskr import create_app
from models import Question, Category

class Basic_Config:
    SQLALCHEMY_DATABASE_URI= 'sqlite:///:memory:'
    TESTING=True


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(Basic_Config)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.seed_category = [
            Category(type='Science'),
            Category(type='Art'),
            Category(type='Geography'),
            Category(type='History'),
            Category(type='Entertainment'),
            Category(type='Sports'),
        ]
        for cat in self.seed_category:
            cat.insert()
     
        self.seed_question = [
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

        for q in self.seed_question:
            q.insert()
    
    def tearDown(self):
        """Executed after reach test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #simple test of db
    def test_initial(self):
        rows = db.session.execute(db.select(Category).order_by(Category.id)).scalars().all()
        categories = [r.type for r in rows]
        self.assertEqual(len(categories),6)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()