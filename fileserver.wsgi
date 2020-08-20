import sys
import os

# Patch that is necessary for mod_wsgi
sys.path.append('/opt/recodex-fileserver')

from fileserver import create_app

def application(environ, start_response):
    flask_app = create_app(environ.get("WORKING_DIRECTORY"))
    return flask_app(environ, start_response)
