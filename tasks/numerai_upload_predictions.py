import os
import sys

import luigi

from numerai_train_and_predict import TrainAndPredict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from targets.numerai_submission import SubmissionTarget


class UploadPredictions(luigi.Task):
    """
    This task uploads a prediction file if it wasn't uploaded before. The file
    name is configured via the filepath parameter.
    """
    dataset_path = luigi.Parameter(
        default='https://datasets.numer.ai/57b4899/numerai_datasets.zip')
    output_path = luigi.Parameter(default='./data/')
    usermail = luigi.Parameter()
    userpass = luigi.Parameter()
    filepath = luigi.Parameter()

    def output(self):
        return SubmissionTarget(self.filepath, self.usermail, self.userpass)

    def requries(self):
        pass

    def run(self):
        self.output().submit()
