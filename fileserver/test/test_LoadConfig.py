import unittest
import io

from fileserver.Config import Config

class TestLoadConfig(unittest.TestCase):
    def test_basic(self):
        input = io.StringIO("""
            working-directory: /tmp/foo/bar
        """)

        config = Config(input)
        self.assertEqual(config.working_directory, "/tmp/foo/bar")

    def test_input_empty(self):
        input = io.StringIO("")

        config = Config(input)
        self.assertEqual(config.working_directory, None)

    def test_input_none(self):
        config = Config(None)
        self.assertEqual(config.working_directory, None)
