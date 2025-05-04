import os
from dotenv import load_dotenv
from trading import start_trading_bot  # importa il tuo main trading loop

load_dotenv()  # carica da /config/progetto_b_bot/.env

if __name__ == "__main__":
    print("🚀 Avvio Progetto B Bot")
    start_trading_bot()
