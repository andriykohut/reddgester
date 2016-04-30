FROM python:3.5.1-slim

COPY . /app/
RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev netcat
RUN pip install -r /app/requirements.txt

EXPOSE 8000
WORKDIR /app

CMD ["nameko", "run", "mailer", "--config=mailer.yaml"]
