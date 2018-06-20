import os
from io import BytesIO
from werkzeug.test import Client
from zipfile import ZipFile

from fileserver import DirectoryStructure


def test_store_submission_and_download_archive(dirs: DirectoryStructure, client: Client):
    job_id = "job-id-xxxx"

    store_response = client.post("/submissions/" + job_id, data={
            "foo.txt": (BytesIO(b"foocontent"), "foo.txt"),
            "bar/baz/bah.txt": (BytesIO(b"bahcontent"), "bar/baz/bah.txt")
    })

    assert store_response.status_code == 200

    assert store_response.json == {
        "archive_path": "/submission_archives/job-id-xxxx.zip",
        "result_path": "/results/job-id-xxxx.zip"
    }

    job_dir = os.path.join(dirs.submission_dir, job_id)

    assert os.path.isdir(job_dir)
    assert os.path.exists(os.path.join(job_dir, "foo.txt"))
    assert os.path.exists(os.path.join(job_dir, "bar", "baz", "bah.txt"))

    fetch_response = client.get(store_response.json["archive_path"])
    assert fetch_response.status_code == 200

    with ZipFile(BytesIO(fetch_response.data)) as archive:
        assert archive.namelist() == [
            'job-id-xxxx/',
            'job-id-xxxx/bar/',
            'job-id-xxxx/foo.txt',
            'job-id-xxxx/bar/baz/',
            'job-id-xxxx/bar/baz/bah.txt'
        ]

    assert os.path.exists(os.path.join(dirs.archive_dir, job_id + ".zip"))
