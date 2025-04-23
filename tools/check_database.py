from sys import platform
import urllib
import yaml
import os
import requests
from bs4 import BeautifulSoup


def load_remote_data():
    hostname = None
    port = None
    url = None

    if platform == 'win32':
        separator = '\\'
    elif platform == 'linux':
        separator = '/'

    remote_desc_path = os.path.dirname(__file__) + separator
    with open(remote_desc_path + "remote.yml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for key, value in data.items():
                if key == "http.hostname":
                    hostname = value
                if key == "http.port":
                    port = value

        except yaml.YAMLError as exc:
            print(exc)

    # this is not beautiful
    url = 'http://' + hostname + ':' + str(port)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    datasets = {}
    for link in soup.find_all('a'):
        anch = link.get('href')
        datasets[anch] = dict()

    for val in datasets.keys():
        reqs = requests.get(url + '/' + val)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        for link in soup.find_all('a'):

            path = link.get('href')
            reqs = requests.get(url + '/' + val + path)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            datasets[val][path] = []
            for data in soup.find_all('a'):
                if str(data.get('href')).endswith('/'):
                    parent_path = data.get('href')
                    reqs = requests.get(url + '/' + val + path + data.get('href'))
                    soup = BeautifulSoup(reqs.text, 'html.parser')

                    sub_path = {}
                    sub_path[parent_path] = []
                    for data in soup.find_all('a'):
                        sub_path[parent_path].append(data.get('href'))

                    datasets[val][path].append(sub_path)
                else:
                    datasets[val][path].append(data.get('href'))

    return url, datasets
