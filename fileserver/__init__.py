from flask import Flask
from flask_script import Manager, Server

from .DirectoryStructure import DirectoryStructure

app = Flask(__name__)
dirs = DirectoryStructure()

import fileserver.views

manager = Manager(app)

