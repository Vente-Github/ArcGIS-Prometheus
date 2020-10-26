import logging
from os import environ

from flask import Flask
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from arcgis_prometheus.utils.arcgis_enterprise import Server
from arcgis_prometheus.utils.health_check_app import make_wsgi_health_check_app
from arcgis_prometheus.utils.metrics import CustomCollector


def connect(username, password, server_base_url):
    logging.info("Connecting to %s", server_base_url)
    server = Server(url=f"{server_base_url}/admin",
                        token_url=f"{server_base_url}/tokens/generateToken",
                        username=username,
                        password=password, initialize=True)
    server.check_connection()
    logging.info("Connected")
    return server


logging.basicConfig(level=logging.INFO)
port = environ.get('PORT', 5000)
username = environ.get('USERNAME', 'admin')
password = environ.get('PASSWORD', 'changeme')
server_base_url = environ.get('SERVER_URL', 'https://arcgisonline.com')
gis_server = connect(username, password, server_base_url)

REGISTRY.register(CustomCollector(gis_server))

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app(REGISTRY),
    '/healthcheck': make_wsgi_health_check_app(gis_server),
})

if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=port)
