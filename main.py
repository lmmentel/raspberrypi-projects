
from datetime import datetime
import json
import logging
import time

import toml
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from sensors.ds18b20 import read_temperature
from sensors.bme280 import read_bme280
from arduino.arduino import read_arduino


# configure logging
logger = logging.getLogger('AWSIoTPythonSDK.core')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

with open('config.toml', 'r') as f:
    config = toml.load(f)

# configure the AWS IoT client
aws_client = AWSIoTMQTTClient(config['awsiot']['client_id'])
aws_client.configureEndpoint(config['awsiot']['endpoint'], 8883)
aws_client.configureCredentials(
    config['awsiot']['root_cert'],
    config['awsiot']['private_key'],
    config['awsiot']['certificate'])
aws_client.configureOfflinePublishQueueing(-1)
aws_client.configureDrainingFrequency(2)
aws_client.configureConnectDisconnectTimeout(10)
aws_client.configureMQTTOperationTimeout(5)

aws_client.connect()

time.sleep(2)
topic = config['device']['topic']


if __name__ == '__main__':

    while True:
        temp = read_temperature(config['ds18b20']['device_dir'])
        logger.info(str(temp))
        tph = read_bme280()
        logger.info(str(tph))
        gasldr = read_arduino()
        logger.info(str(gasldr))

        sensor_msg = {'timestamp': datetime.now().isoformat(), **temp, **tph, **gasldr}
        sensor_msg_json = json.dumps(sensor_msg)
        logger.info(sensor_msg_json)
        aws_client.publish(config['sensors']['topic'], sensor_msg_json, 1)
        logger.info('message published')
        time.sleep(config['sampling'])

