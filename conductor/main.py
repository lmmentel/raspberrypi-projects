
from datetime import datetime
import requests
import toml

with open('config.toml', 'r') as fo:
    config = toml.load(fo)

if __name__ == '__main__':

    print('started: ', datetime.now().isoformat())

    # ping healthcheck
    requests.get(config['healthcheck']['url'])
