function Results() {

  return (
    <div>
      <h1>Kaaviot</h1>

      <h2>Kaavio yhdestä saunakerrasta:</h2>
      <iframe
        src="/sauna.html"
        style={{ width: '80%', height: '500px', border: 'none' }}
        title="Saunadata"
      />

      <h2>Tähän joku uusi:</h2>
      <iframe
        src="/sauna6342.html"
        style={{ width: '80%', height: '500px', border: 'none' }}
        title="Saunadata"
      />

      <h2>Tähän joku uusi:</h2>
      <iframe
        src="/saunomiskerta.html"
        style={{ width: '80%', height: '500px', border: 'none' }}
        title="Saunadata"
      />

      <h2>Kaavio yhdestä saunakerrasta:</h2>
      <iframe
        src="/kesa_talvi.html"
        style={{ width: '80%', height: '500px', border: 'none' }}
        title="kesätalvisauna"
      />
    </div>
  );

}

export default Results