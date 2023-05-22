FROM python:3.11.3-slim-bullseye

RUN apt-get update && \
    apt-get upgrade -y

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]

