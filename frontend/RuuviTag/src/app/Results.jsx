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
    </div>
  );

}

export default Results