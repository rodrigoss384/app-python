# Arquivo Dockerfile para criar a imagem.
FROM python:3.9-slim


WORKDIR /app


COPY ./app/requirements.txt .
COPY ./app/app.py .


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000


CMD ["python", "app.py"]




# By: Rodrigo Souza
