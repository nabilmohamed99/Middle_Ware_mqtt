FROM python:3.10-alpine3.13

# cette ligne permet de ne pas avoir de message d'erreur
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1


WORKDIR /app

COPY ./requirements.txt /app/


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app/


CMD ["gunicorn", 'my.app.wsgi:application', '-b','0.0.0.0:8000']