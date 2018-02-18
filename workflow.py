import os
import luigi

from numerapi.numerapi import NumerAPI

from tasks.numerai_fetch_training_data import FetchAndExtractData
from tasks.numerai_train_and_predict import TrainAndPredict
from tasks.numerai_upload_predictions import UploadPredictions


class Workflow(luigi.Task):
    """
    A luigi task pipeline that fetches the most recent data, trains a model on said data
    and does a submission to the numer.ai website.

    :param: output_path (str):
        path where the data shall be stored, defaults to ``./data/``.
    :param: public_id (str):
        public_id from the API credentials
    :param: secret (str):
        secret from the API credentials
    """
    output_path = luigi.Parameter(default='./data/')
    public_id = luigi.Parameter()
    secret = luigi.Parameter()

    def requires(self):
        """
        Formulates the incoming dependencies, in this case the retrieval of the data for
        the current tournament. Returns the results of the
        :py:class:`tasks.numerai_train_and_predict.TrainAndPredict` task as a way to
        forcefully call the task without depending on it.
        """
        data = FetchAndExtractData(output_path=self.output_path)

        return [
            TrainAndPredict(output_path=self.output_path)
        ]

    def run(self):
        """
        After the incoming dependencies
        (:py:class:`tasks.numerai_fetch_training_data.FetchAndExtractData`, and
        :py:class:`tasks.numerai_train_and_predict.TrainAndPredict`) are done, the only
        thing that's left is the submission of the predictions. This method is
        taking care of this.
        """
        task_deps = self.input()

        for task in task_deps:
            yield UploadPredictions(filepath=task.path,
                                    public_id=self.public_id,
                                    secret=self.secret)
