#!/usr/bin/env bash
set -o allexport
[ -f "/config/progetto_b_bot/.env" ] && source "/config/progetto_b_bot/.env"
set +o allexport

# Avvia metriche Prometheus
python /app/bot/metrics.py &
# Avvia dashboard Flask
python /app/bot/dashboard.py &
# Avvia webhook TradingView
python /app/bot/tradingview_webhook.py &
# Avvia bot principale
python /app/bot/main.py
