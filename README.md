# RuuviTag-Projekti

Tämä projekti on kehitetty RuuviTag-anturin keräämän datan analysointiin ja visualisointiin. Ohjelmisto tarjoaa työkalut yksittäisten saunomiskertojen tarkasteluun, yhdistäen Python-pohjaisen datan esikäsittelyn ja React-pohjaisen modernin verkkokäyttöliittymän.


## Tekijät

Projektin toteutuksesta on vastannut työryhmä:
* [Santeri Aaltonen](https://github.com/aaltsant)
* [Diar Rahimi](https://github.com/rahimidiar)
* [Farhad Rahimi](https://github.com/FakeFake11)
* [Samuel Rooke](https://github.com/samuelrooke)

## Arkkitehtuuri

Projekti jakautuu kahteen pääosaan:

1. **Datan esikäsittely (Python)**
2. **Visualisointi (React)**

## Toiminnot

### Automaattinen session hallinta
Ohjelmisto tunnistaa saunomissession alkamisen lämpötilan noustessa yli 28 celsiusasteen. Data rajataan automaattisesti siten, että visualisointi keskittyy vain olennaiseen ajanjaksoon, sisältäen lyhyet puskurit ennen ja jälkeen aktiivisen vaiheen.

### Löylyjen tunnistusalgoritmi
Löylyjen tunnistus perustuu absoluuttisen kosteuden (g/m³) muutokseen. Absoluuttinen kosteus reagoi suoraan ilmaan lisättyyn vesimäärään riippumatta lämpötilan vaihteluista. Algoritmi tunnistaa äkilliset kosteuspiikit ja merkitsee ne datapisteisiin, jotka välitetään käyttöliittymälle.

### React-visualisointi


## Tekniset tiedot

### Esikäsittely (Python)


### Käyttöliittymä (React)
