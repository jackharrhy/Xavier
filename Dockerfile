FROM python:3

WORKDIR /app

COPY *.py /app/
COPY requirements.txt /app/
COPY .env.dist /app/.env

RUN pip install -r requirements.txt

CMD ["python", "xavier.py"]
