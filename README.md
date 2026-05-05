# RuuviTag-Projekti

RuuviTag-anturin saunadatan analysointiin ja visualisointiin. Python käsittelee CSV-datan ja tunnistaa saunomissessiot sekä löylyt, React-sovellus esittää tulokset interaktiivisina kaavioina.

Julkaistu osoitteessa: https://samuelrooke.github.io/RuuviTag-projekti/

## Tekijät

* [Santeri Aaltonen](https://github.com/aaltsant)
* [Diar Rahimi](https://github.com/rahimidiar)
* [Farhad Rahimi](https://github.com/FakeFake11)
* [Samuel Rooke](https://github.com/samuelrooke)

## Toiminnot

- **Sessioiden tunnistus** – sessio alkaa lämpötilan noustessa yli 28 °C
- **Löylyjen tunnistus** – absoluuttisen kosteuden piikki (>0,8 g/m³) lämpötilan ollessa yli 55 °C
- **Neljä interaktiivista kaaviota:** yksittäinen sessio, lämmitys- ja jäähtymisanalyysi, kuukausittainen käyttö, kesä–talvi-vertailu

## Tekniset tiedot

### Esikäsittely (Python)

| Kirjasto | Käyttötarkoitus |
|----------|-----------------|
| Pandas | CSV-datan lukeminen ja suodattaminen |
| Plotly | HTML-kaavioiden luonti |
| NumPy | Tilastolliset laskutoimitukset |
| Matplotlib | Staattinen visualisointi |

Skriptit hakemistossa `Tiedot/Scriptit/`:
```bash
python kaaviot.py         # Kaikkien kaavioiden generointi
python sauna_mittaus.py   # Yksittäinen sessioanalyysi
```

### Käyttöliittymä (React)

| Teknologia | Versio |
|------------|--------|
| React | 19.2.4 |
| React Router DOM | 7.1.0 |
| Vite | 8.0.0 |

```bash
cd frontend/RuuviTag
npm install
npm run dev      # Kehityspalvelin
npm run build    # Tuotantoversio
npm run deploy   # Julkaisu GitHub Pagesiin
```