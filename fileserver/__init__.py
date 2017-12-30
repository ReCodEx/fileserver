__version__ = "1.2.1"


def create_app(working_directory):
    from flask import Flask
    from .views import create_fileserver_blueprint
    from .DirectoryStructure import DirectoryStructure

    app = Flask(__name__)

    dirs = DirectoryStructure(working_directory)
    app.register_blueprint(create_fileserver_blueprint(dirs))

    return app

