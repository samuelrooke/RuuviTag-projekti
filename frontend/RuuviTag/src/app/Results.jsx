import styles from "../styles/HomePage.module.css";

function Results() {

  return (
    <div>
      <h1>Kaaviot</h1>
      <div>
        <h2>Kaavio yhdestä saunakerrasta:</h2>
        <iframe
          src="/sauna.html"
          style={{ width: '80%', height: '500px', border: 'none' }}
          title="Saunadata"
        />
        <p className={styles.para}>
          Tämä kaavio näyttää, mitä saunassa tapahtuu yhden lämmityskerran aikana, ja se on toteutettu Pythonin Plotly-kirjastolla.
          Punainen viiva kertoo, kuinka lämpötila nousee ensin noin 75 asteeseen ja laskee siitä sitten hitaasti yön yli,
          kun taas siniset piikit ja tähdet paljastavat ne kohdat, kun on heitetty kunnolla löylyä (yhteensä 7 kertaa).
          Kaaviosta näkee hyvin, miten ilma kostuu välittömästi löylyä heittäessä ja miten sauna pysyy
          vielä seuraavana aamunakin selvästi huoneenlämpöä lämpimämpänä.
        </p>
        <div className={styles.repocode}>
          <a href="https://github.com/samuelrooke/RuuviTag-projekti/blob/main/Tiedot/Scriptit/sauna_mittaus.py"
            target="_blank"
            rel="noopener noreferrer"
            className="github-link">
            Tutustu kaavion koodiin GitHubissa!
          </a>
        </div>
      </div>

      <div>
        <h2>Saunan lämpenemisen ja viilentymisen nopeus:</h2>
        <iframe
          src="/sauna6342.html"
          style={{ width: '80%', height: '500px', border: 'none' }}
          title="Saunadata"
        />
        <p className={styles.para}>
          Tämä kaavio näyttää saunan lämpenemiseen ja jäähtymiseen kuluvan ajan minuutteina.
          Kuvaajasta nähdään, että saunan lämpötila nousee huippuunsa (72,9 °C) noin 142 minuutin eli reilun kahden
          tunnin kohdalla lämmityksen aloituksesta. Tämän jälkeen alkaa hidas viilentymisvaihe, joka kestää satoja minuutteja,
          havainnollistaen kuinka pitkään saunan rakenteet varaavat lämpöä varsinaisen saunomisen päätyttyä.
        </p>
        <div className={styles.repocode}>
          <a href="https://github.com/samuelrooke/RuuviTag-projekti"
            target="_blank"
            rel="noopener noreferrer"
            className="github-link">
            Tutustu kaavion koodiin GitHubissa!
          </a>
        </div>
      </div>

      <div>
        <h2>Tähän joku uusikaaavio:</h2>
        <iframe
          src="/saunomiskerta.html"
          style={{ width: '80%', height: '500px', border: 'none' }}
          title="Saunadata"
        />
        <p className={styles.para}>
        </p>
      </div>

      <div>
        <h2>Kaavio yhdestä saunakerrasta:</h2>
        <iframe
          src="/kesa_talvi.html"
          style={{ width: '80%', height: '500px', border: 'none' }}
          title="kesätalvisauna"
        />
        <p className={styles.para}>
          Tämä kaavio vertailee saunan lämpötiloja ja kosteutta kesän ja talven välillä lähes vuoden ajanjaksolla.
          Kuvasta näkyy selvästi, miten kesällä (vihreä ja sininen) saunan peruslämpötila ja ilmankosteus pysyvät korkeammalla ja tasaisempana,
          kun taas talvikuukausina (punainen ja liila) mennään kovemmilla vaihteluilla: lämpötilapiikit ovat terävämpiä ja ilma kuivuu huomattavasti
          nopeammin saunomisen välissä. Kaavio havainnollistaa hyvin, kuinka ulkoilman vuodenaika vaikuttaa suoraan
          saunomisolosuhteisiin ja siihen, kuinka nopeasti tila jäähtyy ja kuivuu.
        </p>
        <div className={styles.repocode}>
          <a href="https://github.com/samuelrooke/RuuviTag-projekti"
            target="_blank"
            rel="noopener noreferrer"
            className="github-link">
            Tutustu kaavion koodiin GitHubissa:
          </a>
        </div>
      </div>
    </div>
  );

}

export default Results