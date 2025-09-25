import { useCallback, useEffect, useMemo, useState } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';

const API = 'http://localhost:5000';

export default function QuestionView() {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [categories, setCategories] = useState({});
  const [currentCategory, setCurrentCategory] = useState(null);
  
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const getQuestions = useCallback(
    async (signal) => {
      const res = await fetch(`${API}/questions?page=${page}`, {
        credentials: 'include',
        signal,
      });
      if (!res.ok) throw new Error('Failed questions');
      const result = await res.json();
      setQuestions(result.questions ?? []);
      setTotalQuestions(result.total_questions ?? 0);
      setCategories(result.categories ?? {});
      setCurrentCategory(result.current_category ?? null);
    },
    [page] // 👈 dependência real que a função usa
  );

  useEffect(() => {
    if (location.state?.reset) {
      setPage(1);
      setCurrentCategory(null);
      const controller = new AbortController();
      getQuestions(controller.signal).catch((err) => {
        if (err?.name !== 'AbortError') {
          alert('Unable to load questions. Please try your request again');
        }
      });

      // limpa o state para não disparar de novo ao navegar
      navigate(location.pathname, { replace: true, state: null });

      return () => controller.abort();
    }
  }, [location.state?.reset, getQuestions, navigate, location.pathname]);

  //
  useEffect(() => {
    const controller = new AbortController();
    getQuestions(controller.signal).catch((err) => {
      if (err?.name !== 'AbortError') {
        alert('Unable to load questions. Please try your request again');
      }
    });
    return () => controller.abort();
  }, [getQuestions]); // 👈 agora é seguro e sem warning

  const selectPage = (num) => setPage(num);

  const createPagination = useMemo(() => {
    const maxPage = Math.ceil((totalQuestions || 0) / 10) || 1;
    return Array.from({ length: maxPage }, (_, i) => i + 1);
  }, [totalQuestions]);

  const getByCategory = async (id) => {
    try {
      const res = await fetch(`${API}/categories/${id}/questions`, { credentials: 'include' });
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
      const res = await fetch(`${API}/questions`, {
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
        const res = await fetch(`${API}/questions/${id}`, {
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
