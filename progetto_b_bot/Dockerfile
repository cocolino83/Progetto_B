FROM python:3.11-slim

WORKDIR /app

# Copia e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia script di avvio e cartella bot
COPY run.sh .
COPY bot/ ./bot/

RUN chmod a+x run.sh

CMD ["bash", "run.sh"]
