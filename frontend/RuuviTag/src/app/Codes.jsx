import koodi from "../codes/sauna_mittaus.py?raw"
import styles from "../styles/HomePage.module.css";

function Codes() {

  return (
    <div>
      <h1>Projektissa käytetyt koodit</h1>
      <h2>Yhden saunakerran kaavion koodi:</h2>

      <pre>
        <code className={styles.code}>{koodi}</code>
      </pre>
    </div>
  );

}

export default Codes
