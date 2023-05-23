FROM python:3.11.3-slim-bullseye

RUN apt-get update && \
    apt-get upgrade -y

WORKDIR /app

COPY lib lib

RUN pip install lib/*

COPY main.py .

CMD ["python", "main.py"]

