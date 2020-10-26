import unittest
from werkzeug.exceptions import InternalServerError
from arcgis_prometheus.utils.arcgis_enterprise import Server


class TestServer(unittest.TestCase):
    def test_shouldReturnIntenalServerError_when_thereIsntConnection(self):
        server_base_url = "http://arcgisonline.com"
        username = "admin"
        password = "changeme"

        server = Server(url=f"{server_base_url}/admin",
                        token_url=f"{server_base_url}/tokens/generateToken",
                        username=username,
                        password=password, initialize=True)

        self.assertRaises(InternalServerError, server.check_connection)


if __name__ == '__main__':
    unittest.main()
