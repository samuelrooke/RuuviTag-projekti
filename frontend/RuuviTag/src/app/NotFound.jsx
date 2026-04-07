import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <div>
      <h1>404 - Page not found</h1>
      <p>Oops! Did you get lost? Lets get back to home.</p>
      <Link to="/">Back to homepage</Link>
    </div>
  );
}

export default NotFound;