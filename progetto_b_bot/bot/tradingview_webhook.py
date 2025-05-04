from flask import Flask, request, jsonify
import yaml
import os
from metrics import record_trade
from bot import decision_engine, buy_token, sell_token, fetch_market_data
from notifiche import send_telegram_message

# Carica config
with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
    cfg = yaml.safe_load(f)

WEBHOOK_SECRET = os.getenv('TRADINGVIEW_WEBHOOK_SECRET') or cfg['tradingview']['webhook_secret']

app = Flask(__name__)

@app.route('/tradingview-alert', methods=['POST'])
def webhook():
    data = request.get_json()
    # Verifica segreto
    if data.get('secret') != WEBHOOK_SECRET:
        return jsonify({'error': 'Invalid secret'}), 403

    symbol = data.get('ticker').split(':')[-1]
    price = float(data.get('close'))
    alert_name = data.get('alert_name')

    # Notifica Telegram
    send_telegram_message(f"🔔 Alert TradingView: {alert_name} su {symbol} @ {price}")

    # Decisione e trade
    token_data = fetch_market_data(symbol)
    action = decision_engine({**token_data, 'price': price})
    if action == 'buy':
        buy_token(symbol)
        record_trade(price)
    elif action == 'sell':
        sell_token(symbol)
        record_trade(price)

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=cfg['dashboard']['port'] + 1)
