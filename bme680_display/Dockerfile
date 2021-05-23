FROM arm32v7/python:3.7-slim-stretch

MAINTAINER lmmentel@gmail.com

COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    i2c-tools \
    libffi-dev \
    ttf-dejavu \
    zlib1g-dev \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libopenjp2-7 \
    libtiff5

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "main.py"]
