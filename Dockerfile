FROM python:latest

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /src

WORKDIR /src

COPY . .

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python -m pip install psycopg2-binary

VOLUME [ "/src" ]