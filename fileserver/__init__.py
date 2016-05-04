from flask_script import Manager, Server
import signal


def create_app(config_path):
    from flask import Flask
    from flask_injector import FlaskInjector
    from .views import fs

    config = load_config(config_path)
    app = Flask(__name__)
    app.register_blueprint(fs)

    def dirs(binder):
        from .DirectoryStructure import DirectoryStructure

        binder.bind(
            DirectoryStructure,
            to = DirectoryStructure(config.working_directory)
        )

    FlaskInjector(app, modules = [dirs], use_annotations = True)

    return app


def load_config(path):
    from .Config import Config

    if path is None:
        config = Config()
    else:
        with open(path) as f:
            config = Config(f)

    return config


class RunServer(Server):
    def __call__(self, app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors):
        def shutdown(*args, **kwargs):
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        super().__call__(app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors)

manager = Manager(create_app)
manager.add_option("--config", "-c", dest = "config_path", help = "Path to the configuration file", default = None)
manager.add_command("runserver", RunServer())

