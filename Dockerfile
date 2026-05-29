FROM python:3.11-slim

WORKDIR /app

# Instala dependências primeiro (layer cacheável)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY app/ .

# Cria o diretório para o banco SQLite persistido via volume
RUN mkdir -p /data

# Expõe a porta da API
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]