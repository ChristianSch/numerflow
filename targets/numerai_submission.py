import os
import sys
import luigi
from numerapi.numerapi import NumerAPI


class SubmissionTarget(luigi.target.Target):
    """
    Implements a submission target to "output" predictions from luigi tasks on
    the numer.ai servers.
    """
    def __init__(self, path, public_id, secret):
        """
        Creates a new SubmissionTarget.

        :param: path (str):
            local path to the predictions csv file
        :param: public_id (str):
            public_id as reported by the numer.ai website when creating API
            credentials
        :param: secret (str):
            secret as reported by the numer.ai website when creating API
            credentials
        """
        self.path = path
        self.fn = os.path.split(path)[1]
        self.apc = NumerAPI(public_id, secret)

    def exists(self):
        """
        Checks if a submission for the file named :py:attr:`path` was uploaded.

        NB: the filename as reported by the server is appended by a random
        string (before the file extension), and we can just access the file
        that was submitted last. This might result in double uploads for the
        same file.
        """
        qry = "query user { user { latestSubmission { filename } } }"
        res = self.apc.raw_query(qry, authorization=True)

        data = res['data']['user']['latestSubmission']

        for d in data:
            if d['filename'].startswith(self.fn.replace('.csv', '')):
                return True

        return False

    def submit(self):
        """
        Submits the predictions to the numer.ai servers and tries to report
        back the status.
        """
        ret = self.apc.upload_predictions(self.path)
        print(self.apc.submission_status())
