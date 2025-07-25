# Imagine de bază
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele
COPY . .

# Instalează dependențele
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expune portul
EXPOSE 8000

# Comanda de rulare
CMD ["python", "run.py"]

# Setează variabila de mediu pentru conexiunea Redis
ENV REDIS_URL=redis://host.docker.internal:6379
