import luigi

from tasks.numerai_train_and_predict import TrainAndPredict
from tasks.numerai_upload_predictions import UploadPredictions


class Workflow(luigi.Task):
    usermail = luigi.Parameter()
    userpass = luigi.Parameter()

    def run(self):
        data = [
            TrainAndPredict()
        ]

        for d in data:
            target = d.output()

            UploadPredictions(filepath=target.path, usermail=self.usermail,
                              userpass=self.userpass)
