FROM python:3.10-slim

RUN mkdir /app
COPY /requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
COPY . /app
