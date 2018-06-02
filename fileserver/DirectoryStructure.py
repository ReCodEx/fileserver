import os
import tempfile


class DirectoryStructure:
    def __init__(self, root=None):
        if root is None:
            self.tmp = tempfile.TemporaryDirectory()
            root = self.tmp.name

        self.root = root

        self.submission_dir = os.path.join(root, "submissions")
        os.makedirs(self.submission_dir, exist_ok=True)

        self.archive_dir = os.path.join(root, "submission_archives")
        os.makedirs(self.archive_dir, exist_ok=True)

        self.result_dir = os.path.join(root, "results")
        os.makedirs(self.result_dir, exist_ok=True)

        self.task_dir = os.path.join(root, "exercises")
        os.makedirs(self.task_dir, exist_ok=True)

        self.attachment_dir = os.path.join(root, "attachments")
        os.makedirs(self.attachment_dir, exist_ok=True)

    def get_submissions_count(self):
        return len(os.listdir(self.submission_dir))

    def get_archives_count(self):
        return len(os.listdir(self.archive_dir))

    def get_results_count(self):
        return len(os.listdir(self.result_dir))

    def get_tasks_count(self):
        return sum([len(files) for r, d, files in os.walk(self.task_dir)])
