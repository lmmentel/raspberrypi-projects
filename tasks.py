from invoke import task

@task
def modeprobe(c):
    '''
    Part of the setup for the one-wire DS18B20 temperature sensor
    '''

    c.sudo('modprobe w1-gpio')
    c.sudo('modprobe w1-therm')
    c.run('ls /sys/bus/w1/devices')

