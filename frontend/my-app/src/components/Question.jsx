import { useState } from 'react';
import '../stylesheets/Question.css';

export default function Question({ question, answer, category, difficulty, questionAction }) {
  const [visibleAnswer, setVisibleAnswer] = useState(false);

  return (
    <div className="Question-holder">
      <div className="Question">{question}</div>
      <div className="Question-status">
        <img
          className="category"
          alt={`${category?.toLowerCase?.()}`}
          src={`${category?.toLowerCase?.()}.svg`}
        />
        <div className="difficulty">Difficulty: {difficulty}</div>
        <img
          src="delete.png"
          alt="delete"
          className="delete"
          onClick={() => questionAction('DELETE')}
        />
      </div>
      <div className="show-answer button" onClick={() => setVisibleAnswer(v => !v)}>
        {visibleAnswer ? 'Hide' : 'Show'} Answer
      </div>
      <div className="answer-holder">
        <span style={{ visibility: visibleAnswer ? 'visible' : 'hidden' }}>
          Answer: {answer}
        </span>
      </div>
    </div>
  );
}
