import luigi

from tasks.numerai_train_and_predict import TrainAndPredict
from tasks.numerai_upload_predictions import UploadPredictions

from controllers.ApiController import ApiController


class Workflow(luigi.Task):
    output_path = luigi.Parameter(default='./data/')
    usermail = luigi.Parameter()
    userpass = luigi.Parameter()

    def run(self):
        apc = ApiController()
        dataset_path = apc.fetch_current_dataset_uri()
        data = [
            TrainAndPredict(dataset_path=dataset_path,
                            output_path=self.output_path)
        ]

        for d in data:
            target = d.output()

            yield UploadPredictions(filepath=target.path,
                                    usermail=self.usermail,
                                    userpass=self.userpass,
                                    dataset_path=dataset_path,
                                    output_path=self.output_path)
