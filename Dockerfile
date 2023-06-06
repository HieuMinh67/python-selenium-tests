FROM python:3.11.3-slim-bullseye

WORKDIR /app

COPY lib lib/

RUN pip install lib/*

COPY main.py .
COPY tests tests/

CMD ["python", "main.py"]

