import requests
from arcgis.gis.server.admin import Server as ArcGISServer
from werkzeug.exceptions import InternalServerError


class Server(ArcGISServer):
    def __init__(self, *args, **kwargs):
        ArcGISServer.__init__(self, *args, **kwargs)

    def check_connection(self):
        if self._con and self._con._token is not None:
            try:
                requests.get(f"{self.url}/info",
                             headers={'Authorization': self._con.token})
            except Exception as e:
                raise InternalServerError('Connection error')
        else:
            raise InternalServerError('Connection error')
