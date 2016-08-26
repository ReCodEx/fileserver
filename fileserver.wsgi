import sys
import os

script_path = os.path.realpath(sys.argv[0])
sys.path.append(os.path.dirname(script_path))

from fileserver import create_app

def application(environ, start_response):
    flask_app = create_app(os.environ.get("WORKING_DIRECTORY"))
    return flask_app(environ, start_response)
