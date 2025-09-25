import { Link } from 'react-router-dom';
import '../stylesheets/Header.css';

export default function Header() {
  return (
    <div className="App-header">
      <h1><Link to={{ pathname: '/', state: { reset: Date.now() } }}>Udacitrivia</Link></h1>
      <h2><Link to="/">List</Link></h2>
      <h2><Link to="/add">Add</Link></h2>
      <h2><Link to="/play">Play</Link></h2>
    </div>
  );
}
