import { useEffect, useRef, useState } from 'react';
import '../stylesheets/FormView.css';

export default function FormView() {
  const [form, setForm] = useState({
    question: '',
    answer: '',
    difficulty: '1',
    category: '1',
  });
  const [categories, setCategories] = useState({});
  const formRef = useRef(null);

  const API = 'http://localhost:5000'

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('${API}/categories', { credentials: 'include' });
        if (!res.ok) throw new Error('Failed categories');
        const data = await res.json();
        setCategories(data.categories || {});
      } catch {
        alert('Unable to load categories. Please try your request again');
      }
    })();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((s) => ({ ...s, [name]: value }));
  };

  const submitQuestion = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          question: form.question,
          answer: form.answer,
          difficulty: Number(form.difficulty),
          category: Number(form.category),
        }),
      });
      if (!res.ok) throw new Error('Failed');
      formRef.current?.reset();
      setForm({ question: '', answer: '', difficulty: '1', category: '1' });
    } catch {
      alert('Unable to add question. Please try your request again');
    }
  };

  return (
    <div id="add-form">
      <h2>Add a New Trivia Question</h2>
      <form className="form-view" id="add-question-form" ref={formRef} onSubmit={submitQuestion}>
        <label>
          Question
          <input type="text" name="question" onChange={handleChange} />
        </label>
        <label>
          Answer
          <input type="text" name="answer" onChange={handleChange} />
        </label>
        <label>
          Difficulty
          <select name="difficulty" onChange={handleChange} defaultValue="1">
            {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}</option>)}
          </select>
        </label>
        <label>
          Category
          <select name="category" onChange={handleChange} defaultValue="1">
            {Object.keys(categories).map((id) => (
              <option key={id} value={id}>{categories[id]}</option>
            ))}
          </select>
        </label>
        <input type="submit" className="button" value="Submit" />
      </form>
    </div>
  );
}
