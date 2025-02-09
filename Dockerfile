
FROM python:3.11-slim-buster

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "bk-store/main.py"]
