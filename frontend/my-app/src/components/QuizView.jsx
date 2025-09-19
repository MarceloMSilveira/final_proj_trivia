import { useEffect, useState } from 'react';
import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

export default function QuizView() {
  const [quizCategory, setQuizCategory] = useState(null); // { type, id }
  const [previousQuestions, setPreviousQuestions] = useState([]);
  const [showAnswer, setShowAnswer] = useState(false);
  const [categories, setCategories] = useState({});
  const [numCorrect, setNumCorrect] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState({});
  const [guess, setGuess] = useState('');
  const [forceEnd, setForceEnd] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('/categories', { credentials: 'include' });
        if (!res.ok) throw new Error('Failed categories');
        const data = await res.json();
        setCategories(data.categories || {});
      } catch {
        alert('Unable to load categories. Please try your request again');
      }
    })();
  }, []);

  const selectCategory = ({ type, id = 0 }) => {
    setQuizCategory({ type, id });
  };

  const getNextQuestion = async () => {
    const prev = [...previousQuestions];
    if (currentQuestion.id) prev.push(currentQuestion.id);

    try {
      const res = await fetch('/quizzes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          previous_questions: prev,
          quiz_category: quizCategory,
        }),
      });
      if (!res.ok) throw new Error('Failed quiz');
      const data = await res.json();
      setShowAnswer(false);
      setPreviousQuestions(prev);
      setCurrentQuestion(data.question || {});
      setGuess('');
      setForceEnd(!data.question);
    } catch {
      alert('Unable to load question. Please try your request again');
    }
  };

  useEffect(() => {
    if (quizCategory) getNextQuestion();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [quizCategory]);

  const evaluateAnswer = () => {
    const formatGuess = guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '').toLowerCase();
    const answerArray = String(currentQuestion.answer || '').toLowerCase().split(' ');
    return answerArray.every((el) => formatGuess.includes(el));
  };

  const submitGuess = (e) => {
    e.preventDefault();
    const isCorrect = evaluateAnswer();
    setNumCorrect((n) => (isCorrect ? n + 1 : n));
    setShowAnswer(true);
  };

  const restartGame = () => {
    setQuizCategory(null);
    setPreviousQuestions([]);
    setShowAnswer(false);
    setNumCorrect(0);
    setCurrentQuestion({});
    setGuess('');
    setForceEnd(false);
  };

  const renderPrePlay = () => (
    <div className="quiz-play-holder">
      <div className="choose-header">Choose Category</div>
      <div className="category-holder">
        <div className="play-category" onClick={() => selectCategory({ type: 'ALL', id: 0 })}>
          ALL
        </div>
        {Object.keys(categories).map((id) => (
          <div
            key={id}
            className="play-category"
            onClick={() => selectCategory({ type: categories[id], id })}
          >
            {categories[id]}
          </div>
        ))}
      </div>
    </div>
  );

  const renderFinalScore = () => (
    <div className="quiz-play-holder">
      <div className="final-header">Your Final Score is {numCorrect}</div>
      <div className="play-again button" onClick={restartGame}>
        Play Again?
      </div>
    </div>
  );

  const renderCorrectAnswer = () => {
    const isCorrect = evaluateAnswer();
    return (
      <div className="quiz-play-holder">
        <div className="quiz-question">{currentQuestion.question}</div>
        <div className={isCorrect ? 'correct' : 'wrong'}>
          {isCorrect ? 'You were correct!' : 'You were incorrect'}
        </div>
        <div className="quiz-answer">{currentQuestion.answer}</div>
        <div className="next-question button" onClick={getNextQuestion}>
          Next Question
        </div>
      </div>
    );
  };

  const renderPlay = () => {
    const ended = previousQuestions.length === questionsPerPlay || forceEnd;
    if (ended) return renderFinalScore();
    if (showAnswer) return renderCorrectAnswer();
    return (
      <div className="quiz-play-holder">
        <div className="quiz-question">{currentQuestion.question}</div>
        <form onSubmit={submitGuess}>
          <input type="text" name="guess" value={guess} onChange={(e) => setGuess(e.target.value)} />
          <input className="submit-guess button" type="submit" value="Submit Answer" />
        </form>
      </div>
    );
  };

  return quizCategory ? renderPlay() : renderPrePlay();
}
