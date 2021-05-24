import concurrent.futures
import logging

from prometheus_client.core import StateSetMetricFamily, CounterMetricFamily, GaugeMetricFamily

STATES = ['started', 'stopped']


def get_service_state(service_status):
    state = {}
    for v in STATES:
        state[v] = service_status.lower() == v
    return state


def add_metric(service, state_metrics, busy_metrics, transactions_metrics):
    statistics = service.statistics
    folder = statistics['summary']['folderName']
    service_name = statistics['summary']['serviceName']
    service_type = statistics['summary']['type']
    service_state = get_service_state(service.status['realTimeState'])
    service_configured_state = service.status['configuredState'].lower()

    state_metrics.add_metric([folder, service_name, service_type, service_configured_state], service_state)

    for machine in statistics['perMachine']:
        machine_name = machine['machineName']
        busy_time = machine['totalBusyTime']
        transactions = machine['transactions']
        busy_metrics.add_metric([folder, service_name, service_type, machine_name], busy_time)
        transactions_metrics.add_metric([folder, service_name, service_type, machine_name], transactions)


class CustomCollector(object):
    def __init__(self, gis_server):
        self.gis_server = gis_server

    def collect(self):
        state_metrics = StateSetMetricFamily("arcgis_service_state", 'Status REST services of ArcGIS',
                                             labels=['folder', 'service_name', 'type', 'configured_state', 'cluster',
                                                     'state'])
        busy_metrics = CounterMetricFamily("arcgis_service_busy_time", 'Time busy time in seconds',
                                           labels=['folder', 'service_name', 'type', 'machine'], unit='seconds')
        transactions_metrics = CounterMetricFamily("arcgis_service_trasactions", 'Number transactions',
                                                   labels=['folder', 'service_name', 'type', 'machine'])

        for folder in self.gis_server.services.folders:
            services = self.gis_server.services.list(folder=folder)
            num_services = len(services)
            logging.info(f"Collecting metrics of {num_services} services inside of folder {folder}")
            if num_services > 0:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor_services:
                    for service in services:
                        executor_services.submit(add_metric, service, state_metrics,
                                                 busy_metrics, transactions_metrics)

        licenses_metrics = self.licenses_metrics()

        yield transactions_metrics
        yield busy_metrics
        yield state_metrics
        yield licenses_metrics

    def licenses_metrics(self):
        metric = GaugeMetricFamily("argis_expiration_license", 'Expiration licenses',
                                   labels=['type', 'name', 'display_name', 'version', 'can_expire'], unit='seconds')

        licenses = self.gis_server.system.licenses
        for extn_type in licenses.keys():
            extns = licenses[extn_type]
            if not isinstance(extns, list):
                extns = [extns]
            for extn in extns:
                extn_name = extn['name']
                extn_display_name = extn['displayName'] if 'displayName' in extn else extn_name
                extn_version = extn['version']
                extn_can_expire = str(extn['canExpire'])
                extn_expirartion = extn['expiration'] / 1000 if extn['canExpire'] else 0
                metric.add_metric([extn_type, extn_name, extn_display_name, extn_version, extn_can_expire],
                                  extn_expirartion)
        return metric
