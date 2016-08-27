import luigi

from tasks.numerai_train_and_predict import TrainAndPredict
from tasks.numerai_upload_predictions import UploadPredictions

from controllers.ApiController import ApiController


class Workflow(luigi.Task):
    output_path = luigi.Parameter(default='./data/')
    usermail = luigi.Parameter()
    userpass = luigi.Parameter()

    def requires(self):
        self.apc = ApiController()
        self.dataset_path = self.apc.fetch_current_dataset_uri()

        return [
                TrainAndPredict(dataset_path=self.dataset_path,
                                output_path=self.output_path)
                ]

    def run(self):
        task_deps = self.input()

        for task in task_deps:
            yield UploadPredictions(filepath=task.path,
                                    usermail=self.usermail,
                                    userpass=self.userpass,
                                    dataset_path=self.dataset_path,
                                    output_path=self.output_path)
