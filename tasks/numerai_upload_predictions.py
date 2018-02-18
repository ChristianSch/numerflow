import os
import sys
import luigi
from .numerai_train_and_predict import TrainAndPredict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from targets.numerai_submission import SubmissionTarget


class UploadPredictions(luigi.Task):
    """
    This task uploads a prediction file if it wasn't uploaded before. The file
    name is configured via the filepath parameter.

    :param: secret (str):
        API secret as generated for the given ``public_id`` by the numer.ai website
    :param: public_id (str):
        chosen API identifier as given by the numer.ai website
    :param: filepath (str):
        path to the file which is to be uploaded
    """
    secret = luigi.Parameter()
    public_id = luigi.Parameter()
    filepath = luigi.Parameter()

    def output(self):
        """
        Produces a :py:class:`targets.numerai_submission.SubmissionTarget` for the current
        round.
        """
        return SubmissionTarget(self.filepath, self.public_id, self.secret)

    def requries(self):
        pass

    def run(self):
        """
        Submits the predictions.
        """
        self.output().submit()
