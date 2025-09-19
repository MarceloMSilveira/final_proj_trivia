import { StrictMode } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import './stylesheets/App.css'
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';

function HeaderWithPath() {
  const { pathname } = useLocation();
  return <Header path={pathname} />;
}

export default function App() {
  return (
    <StrictMode>
      <Router>
        <div className="App">
          <HeaderWithPath />
          <Routes>
            <Route path="/" element={<QuestionView />} />
            <Route path="/add" element={<FormView />} />
            <Route path="/play" element={<QuizView />} />
            {/* rota coringa (equivalente ao "default" do Switch) */}
            <Route path="*" element={<QuestionView />} />
          </Routes>
        </div>
      </Router>
    </StrictMode>
  );
}
