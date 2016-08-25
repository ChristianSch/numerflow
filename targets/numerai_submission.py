import os
import sys
import luigi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.ApiController import ApiController


class SubmissionTarget(luigi.target.Target):
    def __init__(self, path, email, password):
        self.path = path
        self.fn = os.path.split(path)[1]
        self.apic = ApiController()
        self.auth = self.apic.login(email, password)
        self.username = self.auth['username']

    def exists(self):
        subs = self.apic.fetch_submissions()

        for s in subs['submissions']:
            if s['filename'] == self.fn:
                return True

        return False

    def submit(self):
        raise NotImplementedError
