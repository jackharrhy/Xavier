FROM python:3

WORKDIR /app

RUN mkdir commands
COPY commands /app/commands/
RUN mkdir utils
COPY utils /app/utils
COPY *.py /app/
COPY requirements.txt /app/
COPY .env.dist /app/.env

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=0

CMD ["python", "-u", "xavier.py"]
