from flask import Flask
from flask_script import Manager, Server
import signal

from .DirectoryStructure import DirectoryStructure

app = Flask(__name__)
dirs = DirectoryStructure()

import fileserver.views

class RunServer(Server):
    def __call__(self, app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors):
        def shutdown(*args, **kwargs):
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        super().__call__(app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors)

manager = Manager(app)
manager.add_command("runserver", RunServer())

