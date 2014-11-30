#!/usr/bin/env python
"""
API bootstrap file
"""
from flask import Flask, jsonify, g
import sys
import os
import argparse
import logging
from elasticsearch import Elasticsearch

sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../lib')
sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../conf')

import example

logger = logging.getLogger(__name__)

def connect_db():
    """ connect to couchbase """
    try:
        db_client = Elasticsearch()
    except Exception as error:
        raise
    return db_client

db_client = connect_db()


def create_app():
    """ dynamically create the app """
    #app = Flask(__name__, static_url_path='')
    app = Flask(__name__)
    app.config.from_object(__name__)

    #@app.teardown_appcontext
    #def shutdown_session(exception=None):
        #db_session.remove()

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(409)
    @app.errorhandler(500)
    def default_error_handle(error=None):
        """ handle all errors with json output """
        return jsonify(error=str(error), message=error.description,
            success=False), error.code

    ## add each api Blueprint and create the base route
    #from example.v1.api.auth.views import auth
    #app.register_blueprint(auth, url_prefix="/v1/auth")
    #from example.v1.api.users.views import users
    #app.register_blueprint(users, url_prefix="/v1/users")

    return app


def bootstrap(**kwargs):
    """bootstraps the application. can handle setup here"""
    app = create_app()
    app.debug = True
    app.run(host=kwargs['host'], port=kwargs['port'])


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s %(levelname)s %(name)s[%(process)s] : %(funcName)s"
            " : %(message)s"),
        #filename='/var/log/AAA/%s.log' % FILE_NAME
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Hostname or IP address",
        dest="host", type=str, default='0.0.0.0')
    parser.add_argument("--port", help="Port number",
        dest="port", type=int, default=8000)
    kwargs = parser.parse_args()
    bootstrap(**kwargs.__dict__)