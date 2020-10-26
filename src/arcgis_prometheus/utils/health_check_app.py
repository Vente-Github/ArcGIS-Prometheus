from flask import Flask
from werkzeug.exceptions import InternalServerError


def make_wsgi_health_check_app(connection):
    app = Flask(__name__)
    _con = connection

    @app.route('/')
    def index():
        try:
            _con.check_connection()
        except Exception as e:
            raise InternalServerError()
        return "UP"

    return app

    @app.errorhandler(InternalServerError)
    def handle_error_connection_exception(e):
        return e.code, e.description
