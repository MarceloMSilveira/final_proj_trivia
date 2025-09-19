import { useState } from 'react';

export default function Search({ submitSearch }) {
  const [query, setQuery] = useState('');
  const onSubmit = (e) => {
    e.preventDefault();
    submitSearch(query);
  };
  return (
    <form onSubmit={onSubmit}>
      <input
        placeholder="Search questions..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <input type="submit" value="Submit" className="button" />
    </form>
  );
}
