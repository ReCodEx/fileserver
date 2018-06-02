import fileserver
from fileserver.DirectoryStructure import DirectoryStructure
from .utils import hash_file

from flask import request, url_for, send_from_directory, Blueprint, render_template, send_file, jsonify
from tempfile import NamedTemporaryFile
import os
import hashlib
import shutil


def create_fileserver_blueprint(dirs: DirectoryStructure):
    fs = Blueprint("fileserver", __name__)

    @fs.route('/')
    def get_home_page():
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
    def get_submission_archive(id, ext):
        """
        Get a submission archive.
        """

        path = os.path.join(dirs.archive_dir, id)  + ".zip"

        if not os.path.exists(path):
            shutil.make_archive(os.path.splitext(path)[0], "zip", root_dir=dirs.submission_dir, base_dir=id)

        # Send the submission archive
        return send_file(path, attachment_filename="{0}.{1}".format(id, ext), mimetype="application/zip")

    @fs.route('/results/<id>.<ext>')
    def get_result_archive(id, ext):
        """
        Get a result archive.
        """

        return send_from_directory(
            dirs.result_dir,
            "{0}.{1}".format(id, ext)
        )

    @fs.route('/tasks/<hash>')
    @fs.route('/exercises/<hash>')
    def get_task_file(hash):
        """
        Get a task file identified by a SHA-1 hash of its content
        """

        return send_from_directory(
            os.path.join(dirs.task_dir, hash[0]),
            hash
        )

    @fs.route('/submissions/<id>', methods=('GET', 'POST'))
    def store_submission(id):
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

        # Return the path to the archive
        return jsonify({
            "archive_path": url_for('fileserver.get_submission_archive', id=id, ext='zip'),
            "result_path": url_for('fileserver.store_result', id=id, ext='zip')
        })

    @fs.route('/results/<id>.<ext>', methods=('GET', 'PUT'))
    def store_result(id, ext):
        """
        Store the result data of an evaluation.
        This should be done by a worker that processes the submission.
        The result should be a zip archive.
        """

        path = os.path.join(dirs.result_dir, "{0}.{1}".format(id, ext))
        path_tmp = path + ".part"
        with open(path_tmp, 'wb') as f:
            f.write(request.data)

        os.replace(path_tmp, path)

        return jsonify({
            "result": "OK"
        })

    @fs.route('/tasks', methods = ('GET', 'POST'))
    @fs.route('/exercises', methods = ('GET', 'POST'))
    def store_task_files():
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

            if os.path.exists(os.path.join(file_dir, hash)):
                continue

            with open(os.path.join(file_dir, hash), "wb") as f:
                content.seek(0)
                content.save(f)

        return jsonify({
            "result": "OK",
            "files": files
        })

    return fs
