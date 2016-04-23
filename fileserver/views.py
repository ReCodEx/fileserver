from fileserver import app
from fileserver import dirs

from flask import request, url_for, send_from_directory
import os
import json
import tarfile
import hashlib

@app.route('/submission_archives/<id>.<ext>', methods = ('GET'))
def get_submission_archive(id, ext):
    """
    Get a submission archive.
    """

    return send_from_directory(
        dirs.archive_dir, 
        "{0}.{1}".format(id, ext)
    )

@app.route('/results/<id>.<ext>')
def get_result_archive(id, ext):
    """
    Get a result archive.
    """

    return send_from_directory(
        dirs.result_dir,
        "{0}.{1}".format(id, ext)
    )

@app.route('/tasks/<prefix>/<hash>')
def get_task_file(prefix, hash):
    """
    Get a task file identified by a SHA-1 hash of its content
    """

    return send_from_directory(
        os.path.join(dirs.task_dir, os.path.realpath(prefix)), 
        hash
    )

@app.route('/submissions/<id>', methods = ('GET', 'POST'))
def store_submission(id):
    """
    Store files submitted by a user and create an archive for workers convenience.
    Expects that the body of the POST request uses file paths as keys and the 
    content of the files as values.
    """

    # Make a separate directory for the submitted files
    job_dir = os.path.join(dirs.submission_dir, id)
    os.makedirs(job_dir)

    # Save each received file
    for name, content in request.form.items():
        # Get the directory of the file path and create it, if necessary
        dirname = os.path.dirname(name)
        if dirname:
            os.makedirs(os.path.join(job_dir, dirname), exist_ok = True)

        # Save the file
        with open(os.path.join(job_dir, name), 'w') as f:
            f.write(content)

    # Make an archive that contains the submitted files
    archive_path = os.path.join(dirs.archive_dir, id + '.tar.gz')
    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(job_dir, arcname = id)

    # Return the path to the archive
    return json.dumps({
        "archive_path": url_for('get_submission_archive', id = id, ext = 'tar.gz'),
        "result_path": url_for('store_result', id = id, ext = 'zip')
    })

@app.route('/results/<id>.<ext>', methods = ('GET', 'PUT'))
def store_result(id, ext):
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

@app.route('/tasks', methods = ('GET', 'POST'))
def store_task_files():
    """
    Store supplementary task files under hashes of their contents.
    """

    files = {}

    for name, content in request.form.items():
        hash = hashlib.sha1(content.encode()).hexdigest()
        prefix = hash[0]
        files[name] = url_for("get_task_file", prefix = prefix, hash = hash)

        file_dir = os.path.join(dirs.task_dir, prefix)
        os.makedirs(file_dir, exist_ok = True)

        with open(os.path.join(file_dir, hash), "wb") as f:
            f.write(content.encode())

    return json.dumps({
        "result": "OK",
        "files": files
    })
