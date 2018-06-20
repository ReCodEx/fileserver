import pytest
from tempfile import TemporaryDirectory

from fileserver import create_app
from fileserver.DirectoryStructure import DirectoryStructure


@pytest.fixture()
def dirs():
    with TemporaryDirectory() as directory:
        yield DirectoryStructure(directory)


@pytest.fixture()
def app(dirs):
    yield create_app(dirs.root)
