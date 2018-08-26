FROM arm32v7/python:3.6.6-slim-stretch

MAINTAINER lmmentel@gmail.com

COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential i2c-tools libffi-dev
RUN pip install pipenv

#RUN pipenv install --system --deploy
RUN pipenv install

CMD ["pipenv", "run", "python", "main.py"]
