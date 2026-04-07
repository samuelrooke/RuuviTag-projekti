import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import Codes from './Codes';
import Results from './Results';
import NotFound from './NotFound';
import NavBar from './NavBar';

function MainPage() {

  return (
    <>
      <NavBar />
      <div>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/tulokset" element={<Results />} />
          <Route path="/koodit" element={<Codes />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </>
  );
}

export default MainPage
