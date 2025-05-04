from prometheus_client import start_http_server, Counter, Gauge
import yaml
import os

# Carica porta dal config
with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
    cfg = yaml.safe_load(f)

PROM_PORT = cfg['prometheus']['port']

# Definizione metriche
TRADE_COUNTER = Counter('bot_trades_total', 'Numero di trade eseguiti')
LAST_PRICE = Gauge('bot_last_price', 'Ultimo prezzo elaborato')

def start_metrics():
    """Avvia il server HTTP di Prometheus."""
    start_http_server(PROM_PORT)
    print(f"Prometheus metrics listening on port {PROM_PORT}")

def record_trade(price):
    """Chiamare ad ogni trade per aggiornare le metriche."""
    TRADE_COUNTER.inc()
    LAST_PRICE.set(price)

if __name__ == '__main__':
    start_metrics()
    import time
    # loop di test
    while True:
        record_trade(1000)  # esempio
        time.sleep(5)
