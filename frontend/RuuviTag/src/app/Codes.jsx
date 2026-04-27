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

      <div>
        <h2>Näin koodi toimii:</h2>
        <p>
          Tämä Python-skripti vastaa yhden saunakerran prosessoinnista ja visualisoinnista. Koodi lukee sensorin keräämän datan CSV-tiedostosta
          ja käyttää Pandas-kirjastoa datan siivoamiseen sekä Plotly-kirjastoa interaktiivisen kaavion luomiseen.
        </p>
        
        <ul>
          <li>Datan rajaus: Skripti tunnistaa automaattisesti saunomissessioiden alkamis- ja päättymisajat lämpötilan perusteella.</li>
          <li>Löylyjen tunnistus: Koodi sisältää logiikan, joka tunnistaa löylynheiton ilmankosteuden äkillisistä muutoksista ja merkitsee ne kaavioon tähdillä.</li>
          <li>Visualisointi: Se luo yhdistelmäkaavion, jossa lämpötila ja kosteus näkyvät omilla asteikoillaan, jotta niiden välistä suhdetta on helppo seurata.</li>
        </ul>

        <p>
          Koska tällä sivulla on esillä vain tämän kyseisen kaavion muodostamiseen käytetty logiikka, voit tutustua projektin koko lähdekoodiin
          ja muutenkin meidän projektiimme GitHub-repositoriossamme:
        </p>

        <div className={styles.repo}>
          <a href="https://github.com/samuelrooke/RuuviTag-projekti"
            target="_blank"
            rel="noopener noreferrer"
            className="github-link">
            Tutustu koko projektiin GitHubissa
          </a>
        </div>
        </div>
    </div>
  );

}

export default Codes
