import json
import os
import unittest
from unittest.mock import Mock, patch

from werkzeug.datastructures import ImmutableMultiDict

from fileserver import dirs
from fileserver.views import store_submission
import fileserver


def url_for(function, **kwargs):
    kwargs['function'] = function
    return kwargs


class TestStoreSubmission(unittest.TestCase):
    @patch('fileserver.views.request')
    @patch('fileserver.views.url_for', side_effect = url_for)
    def test_basic(self, mock_request, mock_url_for):
        mock_request.form = ImmutableMultiDict([
            ("foo.txt", "foocontent"),
            ("bar/baz/bah.txt", "bahcontent")
        ])

        job_id = "job-id-xxxx"

        expected_response = {
            "archive_path": {"function": "get_submission_archive", "id": job_id, "ext": "tar.gz"},
            "result_path": {"function": "store_result", "id": job_id, "ext": "zip"}
        }

        actual_response = json.loads(store_submission(job_id))
        self.assertEqual(expected_response, actual_response)

        job_dir = os.path.join(dirs.submission_dir, job_id)
        self.assertTrue(os.path.isdir(job_dir))

        self.assertTrue(os.path.exists(os.path.join(dirs.archive_dir, job_id + ".tar.gz")))


if __name__ == '__main__':
    unittest.main()
