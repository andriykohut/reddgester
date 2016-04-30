FROM python:3.5.1-slim

COPY . /app/
RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev
RUN pip install -r /app/requirements.txt

EXPOSE 8080
WORKDIR /app

CMD python api.py runserver --amqp-uri amqp://guest:guest@127.0.0.1:5672
