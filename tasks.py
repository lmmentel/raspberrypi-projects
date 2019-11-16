from invoke import task
import toml


with open('config.toml', 'r') as f:
    config = toml.load(f)


@task
def modeprobe(c):
    '''
    Part of the setup for the one-wire DS18B20 temperature sensor
    '''

    c.sudo('modprobe w1-gpio')
    c.sudo('modprobe w1-therm')
    c.run('ls /sys/bus/w1/devices')


@task
def testaws(c):

    c.run('which python')
    c.run('python /home/pi/projects/aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py'
          ' -e {0:s}'.format(config['awsiot']['endpoint']) +
          ' -r {0:s}'.format(config['awsiot']['root_cert']) +
          ' -c {0:s}'.format(config['awsiot']['certificate']) +
          ' -k {0:s}'.format(config['awsiot']['private_key']))

@task
def ds18b20(c):

    from sensors.ds18b20 import get_temperature

    print(get_temperature(config['ds18b20']['device_dir']))

