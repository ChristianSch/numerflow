import luigi

from tasks.numerai_train_and_predict import TrainAndPredict
from tasks.numerai_upload_predictions import UploadPredictions


class Workflow(luigi.Task):
    dataset_path = luigi.Parameter(
        default='https://datasets.numer.ai/57b4899/numerai_datasets.zip')
    output_path = luigi.Parameter(default='./data/')
    usermail = luigi.Parameter()
    userpass = luigi.Parameter()

    def run(self):
        data = [
            TrainAndPredict()
        ]

        for d in data:
            target = d.output()

            UploadPredictions(filepath=target.path,
                              usermail=self.usermail,
                              userpass=self.userpass,
                              dataset_path=self.dataset_path,
                              output_path=self.output_path)
