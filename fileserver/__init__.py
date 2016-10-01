from flask_script import Manager, Server
import signal

__version__ = "0.1.0"


def create_app(working_directory):
    from flask import Flask
    from flask_injector import FlaskInjector
    from .views import fs

    app = Flask(__name__)
    app.register_blueprint(fs)

    def dirs(binder):
        from .DirectoryStructure import DirectoryStructure

        binder.bind(
            DirectoryStructure,
            to=DirectoryStructure(working_directory)
        )

    FlaskInjector(app, modules=[dirs], use_annotations=True)

    return app


class RunServer(Server):
    def __call__(self, app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors):
        def shutdown(*args, **kwargs):
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        super().__call__(app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors)

manager = Manager(create_app)
manager.add_option("--directory", dest="working_directory", help="The directory where files are stored", default=None)
manager.add_command("runserver", RunServer())

