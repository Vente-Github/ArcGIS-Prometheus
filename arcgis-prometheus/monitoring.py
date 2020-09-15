import concurrent.futures
import logging
import time
from os import environ

from arcgis.gis.server.admin import Server
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, StateSetMetricFamily

STATES = ['started', 'stopped']


def connect(username, password, server_base_url):
    logging.info("Connecting to %s", server_base_url)
    gis_server = Server(url=f"{server_base_url}/arcgis/admin",
                        token_url=f"{server_base_url}/arcgis/tokens/generateToken",
                        username=username,
                        password=password)
    logging.info("Connected")
    return gis_server


def get_service_state(service_status):
    state = {}
    for v in STATES:
        state[v] = service_status.lower() == v
    return state


def add_metric(service, metric):
    statistics = service.statistics
    folder = statistics['summary']['folderName']
    service_name = statistics['summary']['serviceName']
    service_type = statistics['summary']['type']
    service_state = get_service_state(service.status['realTimeState'])

    metric.add_metric([folder, service_name, service_type], service_state)


class CustomCollector(object):
    def __init__(self, gis_server):
        self.gis_server = gis_server

    def collect(self):
        metrics = StateSetMetricFamily("arcgis_service_state", 'Status REST services of ArcGIS',
                                       labels=['folder', 'service_name', 'type', 'state'])
        for folder in self.gis_server.services.folders:
            services = self.gis_server.services.list(folder=folder)
            num_services = len(services)
            logging.info(f"Collecting metrics of {num_services} services inside of folder {folder}")
            if num_services > 0:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor_services:
                    for service in services:
                        executor_services.submit(add_metric, service, metrics)
        yield metrics


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    port = environ.get('PORT', 8000)
    start_http_server(port)

    username = environ.get('USERNAME', 'admin')
    password = environ.get('PASSWORD', 'changeme')
    server_base_url = environ.get('SERVER_URL', 'https://arcgisonline.com')
    gis_server = connect(username, password, server_base_url)
    REGISTRY.register(CustomCollector(gis_server))
    while True:
        time.sleep(1)
