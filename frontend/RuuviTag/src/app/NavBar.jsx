import { Link } from 'react-router-dom';
import styles from '../styles/App.module.css';

function NavBar() {

    return (
        <nav className={styles.nav}>
            <Link to="/">Koti</Link>
            <Link to="/tulokset">Tulokset</Link>
            <Link to="/koodit">Koodit</Link>
        </nav>
    );
}

export default NavBar;
