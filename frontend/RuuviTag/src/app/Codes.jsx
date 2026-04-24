import koodi from "../codes/sauna_mittaus.py?raw"

function Codes() {

  return (
    <div>
      <h1>Projektissa käytetyt koodit</h1>
      <h2>Yhden saunakerran kaavion koodi:</h2>
      
      <pre style={{
        textAlign: 'left',
        maxWidth: '900px',
        margin: '40px auto'}}>
        <code>
            {koodi}
        </code>
      </pre>
    </div>
  );

}

export default Codes
