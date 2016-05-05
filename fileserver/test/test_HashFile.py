import unittest
import io
import hashlib

from fileserver.utils import hash_file

class TestHashFile(unittest.TestCase):
    def test_large(self):
        data = io.BytesIO(b"a" * (2 ** 20))
        expected = hashlib.sha1(data.read())

        data.seek(0)
        actual = hashlib.sha1()
        actual = hash_file(actual, data)

        self.assertEqual(expected.hexdigest(), actual.hexdigest())

    def test_empty(self):
        data = io.BytesIO(b"")
        expected = hashlib.sha1(data.read())

        data.seek(0)
        actual = hashlib.sha1()
        actual = hash_file(actual, data)

        self.assertEqual(expected.hexdigest(), actual.hexdigest())

    def test_small(self):
        data = io.BytesIO(b"" * 100)
        expected = hashlib.sha1(data.read())

        data.seek(0)
        actual = hashlib.sha1()
        actual = hash_file(actual, data)

        self.assertEqual(expected.hexdigest(), actual.hexdigest())

    def test_unicode_throws(self):
        data = io.StringIO("a" * 100)
        actual = hashlib.sha1()

        with self.assertRaises(TypeError) as context:
            actual = hash_file(actual, data)
