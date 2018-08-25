FROM arm32v7/3.7.0-slim-stretch

MAINTAINER lmmentel@gmail.com

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "main.py"]