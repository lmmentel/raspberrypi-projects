
import re
import socket
from subprocess import run
from time import sleep

from tabulate import tabulate
import psutil
from psutil._common import bytes2human


def get_gpu_temp():
    '''
    Get the GPU temperature
    '''

    proc = run(['vcgencmd', 'measure_temp'], capture_output=True)
    pattern = r'.*=(\d+\.\d+)'
    string = proc.stdout.decode('utf-8')

    match = re.match(pattern, string)
    if match:
        return float(match.group(1))
    else:
        raise ValueError('no match found in: '.format(string))


def read_metrics(host):
    '''
    Collect metric about the raspberry pi and return a dict
    '''


    metrics = dict()

    # CPU usage
    cpu = psutil.cpu_percent(interval=1, percpu=False)
    metrics[f'{host}.cpu_percent_used'] = cpu
    # print(psutil.getloadavg())
    # print(psutil.cpu_freq())
    # memory usage
    mem = psutil.virtual_memory()
    metrics[f'{host}.mem_percent_used'] = mem.percent
    metrics[f'{host}.mem_available'] = bytes2human(mem.available)
    # disk usage
    disk = psutil.disk_usage('/')
    metrics[f'{host}.disk_percent_used'] = disk.percent
    metrics[f'{host}.disk_free'] = bytes2human(disk.free)
    # CPU temperature
    temp = psutil.sensors_temperatures(fahrenheit=False)
    #metrics['cpu_temp_c'] = temp['cpu-thermal'][0].current
    # GPU temperature
    gpu = get_gpu_temp()
    metrics[f'{host}.gpu_temp_c'] = gpu

    return metrics

if __name__ == '__main__':

    hostname = socket.gethostname()

    while True:
        metrics = get_metrics(hostname)
        print(tabulate([metrics],  tablefmt='plain',
                floatfmt=".2f", headers='keys'))
        sleep(1)

