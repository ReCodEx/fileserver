import os
import tempfile

class DirectoryStructure:
    def __init__(self, root = None):
        if root is None:
            self.tmp = tempfile.TemporaryDirectory()
            root = self.tmp.name

        self.submission_dir = os.path.join(root, "submissions")
        os.makedirs(self.submission_dir, exist_ok = True)

        self.archive_dir = os.path.join(root, "submission_archives")
        os.makedirs(self.archive_dir, exist_ok = True)

        self.result_dir = os.path.join(root, "results")
        os.makedirs(self.result_dir, exist_ok = True)

        self.task_dir = os.path.join(root, "tasks")
        os.makedirs(self.task_dir, exist_ok = True)

