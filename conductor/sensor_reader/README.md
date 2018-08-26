
# Python sensor readed

To build the image

```
docker image build -t lmmentel/sensor-reader .
```

The container needs to be started in privileged mode ro read from GPIO

```
docker run --privileged -d --name sensors lmmentel/sensor-reader
```
