import { useEffect, useMemo, useState } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';

export default function QuestionView() {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [categories, setCategories] = useState({});
  const [currentCategory, setCurrentCategory] = useState(null);

  const getQuestions = async () => {
    try {
      const res = await fetch(`/questions?page=${page}`, { credentials: 'include' });
      if (!res.ok) throw new Error('Failed questions');
      const result = await res.json();
      setQuestions(result.questions || []);
      setTotalQuestions(result.total_questions || 0);
      setCategories(result.categories || {});
      setCurrentCategory(result.current_category ?? null);
    } catch {
      alert('Unable to load questions. Please try your request again');
    }
  };

  useEffect(() => { getQuestions(); }, [page]);

  const selectPage = (num) => setPage(num);

  const createPagination = useMemo(() => {
    const maxPage = Math.ceil((totalQuestions || 0) / 10) || 1;
    return Array.from({ length: maxPage }, (_, i) => i + 1);
  }, [totalQuestions]);

  const getByCategory = async (id) => {
    try {
      const res = await fetch(`/categories/${id}/questions`, { credentials: 'include' });
      if (!res.ok) throw new Error('Failed by category');
      const result = await res.json();
      setQuestions(result.questions || []);
      setTotalQuestions(result.total_questions || 0);
      setCurrentCategory(result.current_category ?? null);
    } catch {
      alert('Unable to load questions. Please try your request again');
    }
  };

  const submitSearch = async (searchTerm) => {
    try {
      const res = await fetch('/questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ searchTerm }),
      });
      if (!res.ok) throw new Error('Failed search');
      const result = await res.json();
      setQuestions(result.questions || []);
      setTotalQuestions(result.total_questions || 0);
      setCurrentCategory(result.current_category ?? null);
      setPage(1);
    } catch {
      alert('Unable to load questions. Please try your request again');
    }
  };

  const questionAction = (id) => async (action) => {
    if (action === 'DELETE' && window.confirm('are you sure you want to delete the question?')) {
      try {
        const res = await fetch(`/questions/${id}`, {
          method: 'DELETE',
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Failed delete');
        await getQuestions();
      } catch {
        alert('Unable to load questions. Please try your request again');
      }
    }
  };

  return (
    <div className="question-view">
      <div className="categories-list">
        <h2 onClick={() => getQuestions()}>Categories</h2>
        <h2>
          Questions{currentCategory ? ` — ${currentCategory}` : ''}
        </h2>

        <ul>
          {Object.keys(categories).map((id) => (
            <li key={id} onClick={() => getByCategory(id)}>
              {categories[id]}
              <img
                className="category"
                alt={`${String(categories[id]).toLowerCase()}`}
                src={`${String(categories[id]).toLowerCase()}.svg`}
              />
            </li>
          ))}
        </ul>
        <Search submitSearch={submitSearch} />
      </div>
      <div className="questions-list">
        <h2>Questions</h2>
        {questions.map((q) => (
          <Question
            key={q.id}
            question={q.question}
            answer={q.answer}
            category={categories[q.category]}
            difficulty={q.difficulty}
            questionAction={questionAction(q.id)}
          />
        ))}
        <div className="pagination-menu">
          {createPagination.map((n) => (
            <span
              key={n}
              className={`page-num ${n === page ? 'active' : ''}`}
              onClick={() => selectPage(n)}
            >
              {n}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
