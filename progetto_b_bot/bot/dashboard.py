from flask import Flask, render_template_string
import yaml
import os
import pandas as pd

app = Flask(__name__)

# Template HTML molto semplice
TEMPLATE = """
<!doctype html>
<html>
<head><title>Progetto B Bot Dashboard</title></head>
<body>
  <h1>Dashboard Progetto B Bot</h1>
  <p>Ultimo prezzo: {{ last_price }}</p>
  <p>Trade eseguiti: {{ trades }}</p>
  <h2>Storico Operazioni</h2>
  <table border="1">
    <tr><th>Timestamp</th><th>Asset</th><th>Azione</th><th>Prezzo</th></tr>
    {% for op in ops %}
    <tr>
      <td>{{ op.timestamp }}</td>
      <td>{{ op.asset }}</td>
      <td>{{ op.action }}</td>
      <td>{{ op.price }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>
"""

# Simula lettura CSV con storico
LOG_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'log_trading.csv')

@app.route('/')
def dashboard():
    # Ultime metriche (in un sistema reale andresti a Prometheus)
    last_price = '—'
    trades = '—'
    # Carica storico
    ops = []
    if os.path.isfile(LOG_CSV):
        df = pd.read_csv(LOG_CSV)
        ops = df.tail(10).to_dict(orient='records')
        trades = len(df)
        if 'price' in df.columns:
            last_price = df.iloc[-1]['price']
    return render_template_string(TEMPLATE,
                                  last_price=last_price,
                                  trades=trades,
                                  ops=ops)

if __name__ == '__main__':
    # Porta dal config
    with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
        cfg = yaml.safe_load(f)
    app.run(host='0.0.0.0', port=cfg['dashboard']['port'])
