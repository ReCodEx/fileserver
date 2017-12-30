import json
import os
import unittest
from unittest.mock import Mock, patch

from werkzeug.datastructures import ImmutableMultiDict
from fileserver.DirectoryStructure import DirectoryStructure

from fileserver import create_app


def url_for(function, **kwargs):
    kwargs['function'] = function
    return kwargs


class TestStoreSubmission(unittest.TestCase):
    @patch('fileserver.views.request')
    @patch('fileserver.views.url_for', side_effect = url_for)
    def test_basic(self, mock_request, mock_url_for):
        dirs = DirectoryStructure()
        app = create_app(dirs.root)
        client = app.test_client()

        job_id = "job-id-xxxx"

        expected_response = {
            "archive_path": {"function": "fileserver.get_submission_archive", "id": job_id, "ext": "zip"},
            "result_path": {"function": "fileserver.store_result", "id": job_id, "ext": "zip"}
        }

        actual_response = json.loads(client.post("/submissions/" + job_id, data=ImmutableMultiDict([
            ("foo.txt", "foocontent"),
            ("bar/baz/bah.txt", "bahcontent")
        ])).data)

        self.assertEqual(expected_response, actual_response)

        job_dir = os.path.join(dirs.submission_dir, job_id)
        self.assertTrue(os.path.isdir(job_dir))

        self.assertTrue(os.path.exists(os.path.join(dirs.archive_dir, job_id + ".zip")))


if __name__ == '__main__':
    unittest.main()
