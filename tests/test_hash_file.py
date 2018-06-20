import io
import hashlib

import pytest

from fileserver.utils import hash_file


def test_large():
    data = io.BytesIO(b"a" * (2 ** 20))
    expected = hashlib.sha1(data.read())

    data.seek(0)
    actual = hashlib.sha1()
    actual = hash_file(actual, data)

    assert expected.hexdigest() == actual.hexdigest()


def test_empty():
    data = io.BytesIO(b"")
    expected = hashlib.sha1(data.read())

    data.seek(0)
    actual = hashlib.sha1()
    actual = hash_file(actual, data)

    assert expected.hexdigest() == actual.hexdigest()


def test_small():
    data = io.BytesIO(b"a" * 100)
    expected = hashlib.sha1(data.read())

    data.seek(0)
    actual = hashlib.sha1()
    actual = hash_file(actual, data)

    assert expected.hexdigest() == actual.hexdigest()


def test_unicode_throws():
    data = io.StringIO("a" * 100)
    actual = hashlib.sha1()

    with pytest.raises(TypeError):
        hash_file(actual, data)
