import "../styles/HomePage.module.css";

function HomePage() {
  return (
    <div>
      <h1>RuuviTag Sauna -projekti</h1>

      <container className="project-section">
        <h2>Mikä on RuuviTag?</h2>
        <p>
          RuuviTag on suomalainen, avoimeen lähdekoodiin perustuva Bluetooth-anturi,
          joka mittaa ympäristön olosuhteita. Se mittaa lämpötilaa, ilmankosteutta,
          ilmanpainetta ja liikettä. RuuviTag on suunniteltu kestämään vaativiakin olosuhteita,
          mikä tekee siitä täydellisen työkalun esimerkiksi saunan seurantaan.
        </p>
      </container>

      <container className="project-section">
        <h2>Projektistamme</h2>
        <p>
          Tutkimme projektissamme saunan lämpötilan ja ilmankosteuden dynamiikkaa.
          Käytimme RuuviTagia keräämään reaaliaikaista dataa siitä, miten löylynheitto
          vaikuttaa saunailmaan ja kuinka tasaisesti lämpö jakautuu lämmityksen aikana.
          Tavoitteenamme oli luoda selkeä kuva saunomisen fysiikasta datan valossa.
        </p>
        <ul>
          <li><strong>Miksi:</strong> Halusimme yhdistää perinteisen saunomisen ja modernin teknologian.</li>
          <li><strong>Miten:</strong> Mittasimme dataa usean saunakerran ajan ja analysoimme tulokset.</li>
        </ul>
      </container>

      <container className="project-section">
        <h2>Projektista vastasivat:</h2>
        <ul>
          <li>Santeri Aaltonen</li>
          <li>Samuel Rooke</li>
          <li>Farhad Rahimi</li>
          <li>Diar Rahimi</li>
        </ul>
      </container>
    </div>
  );
}

export default HomePage;