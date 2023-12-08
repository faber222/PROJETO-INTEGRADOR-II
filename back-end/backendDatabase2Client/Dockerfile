FROM python:3.8

WORKDIR /app

# Copie o código Python e o arquivo de requisitos
COPY dbClient.py .
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

CMD ["python", "dbClient.py"]