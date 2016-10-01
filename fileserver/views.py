import fileserver
from fileserver.DirectoryStructure import DirectoryStructure
from .utils import hash_file

from flask import request, url_for, send_from_directory, Blueprint, render_template
import os
import json
import hashlib
import shutil

fs = Blueprint("fileserver", __name__)


@fs.route('/')
def get_home_page(dirs: DirectoryStructure):
    """
    Get simple welcome page.
    """

    stats = [
        ("Results", dirs.get_results_count()),
        ("Submission archives", dirs.get_archives_count()),
        ("Submissions", dirs.get_submissions_count()),
        ("Tasks", dirs.get_tasks_count())
    ]
    return render_template('index.html',
                           version=fileserver.__version__,
                           stats=stats)


@fs.route('/submission_archives/<id>.<ext>')
def get_submission_archive(id, ext, dirs: DirectoryStructure):
    """
    Get a submission archive.
    """

    return send_from_directory(
        dirs.archive_dir,
        "{0}.{1}".format(id, ext)
    )


@fs.route('/results/<id>.<ext>')
def get_result_archive(id, ext, dirs: DirectoryStructure):
    """
    Get a result archive.
    """

    return send_from_directory(
        dirs.result_dir,
        "{0}.{1}".format(id, ext)
    )


@fs.route('/tasks/<hash>')
def get_task_file(hash, dirs: DirectoryStructure):
    """
    Get a task file identified by a SHA-1 hash of its content
    """

    return send_from_directory(
        os.path.join(dirs.task_dir, hash[0]),
        hash
    )


@fs.route('/submissions/<id>', methods=('GET', 'POST'))
def store_submission(id, dirs: DirectoryStructure):
    """
    Store files submitted by a user and create an archive for workers convenience.
    Expects that the body of the POST request uses file paths as keys and the 
    content of the files as values.
    """

    # Make a separate directory for the submitted files
    job_dir = os.path.join(dirs.submission_dir, id)
    os.makedirs(job_dir, exist_ok=True)

    # Save each received file
    for name, content in request.files.items():
        # Get the directory of the file path and create it, if necessary
        dirname = os.path.dirname(name)
        if dirname:
            os.makedirs(os.path.join(job_dir, dirname), exist_ok=True)

        # Save the file
        with open(os.path.join(job_dir, name), 'wb') as f:
            content.save(f)

    # Make an archive that contains the submitted files
    shutil.make_archive(os.path.join(dirs.archive_dir, id), "zip", root_dir=dirs.submission_dir, base_dir=id)

    # Return the path to the archive
    return json.dumps({
        "archive_path": url_for('fileserver.get_submission_archive', id=id, ext='zip'),
        "result_path": url_for('fileserver.store_result', id=id, ext='zip')
    })


@fs.route('/results/<id>.<ext>', methods=('GET', 'PUT'))
def store_result(id, ext, dirs: DirectoryStructure):
    """
    Store the result data of an evaluation.
    This should be done by a worker that processes the submission.
    The result should be a zip archive.
    """

    path = os.path.join(dirs.result_dir, "{0}.{1}".format(id, ext))
    with open(path, 'wb') as f:
        f.write(request.data)

    return json.dumps({
        "result": "OK"
    })


@fs.route('/tasks', methods=('GET', 'POST'))
def store_task_files(dirs: DirectoryStructure):
    """
    Store supplementary task files under hashes of their contents.
    """

    files = {}

    for name, content in request.files.items():
        hash = hash_file(hashlib.sha1(), content).hexdigest()
        prefix = hash[0]
        files[name] = url_for("fileserver.get_task_file", hash=hash)

        file_dir = os.path.join(dirs.task_dir, prefix)
        os.makedirs(file_dir, exist_ok=True)

        with open(os.path.join(file_dir, hash), "wb") as f:
            content.seek(0)
            content.save(f)

    return json.dumps({
        "result": "OK",
        "files": files
    })
