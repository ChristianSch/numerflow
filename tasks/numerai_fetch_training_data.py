import os
import sys
from numerapi.numerapi import NumerAPI
import luigi


class FetchAndExtractData(luigi.Task):
    """
    Fetches the most recent dataset and extracts the contents to the given
    path if not yet done (default path is ``./data``).

    :param: output_path:
        (relative) path where the data should be written to. Defaults to
        ``./data``. Default signature is
        ``FetchAndExtractData(output_path='./data')``.

    ::

        data
        ├── numerai_dataset_95
        │   ├── example_model.py
        │   ├── example_model.r
        │   ├── example_predictions.csv
        │   ├── numerai_tournament_data.csv
        │   └── numerai_training_data.csv
        └── numerai_dataset_95.zip

    """
    output_path = luigi.Parameter(default='./data/')

    def output(self):
        """
        Manages the files to be written and determines their existence.
        This is determined by checking all the listed files below. If any
        of them does not exist, :py:func:`run` is evoked.

        :returns:
            A ``dict`` with the following keys:

            * ``zipfile``: original file as downloaded
            (``numerai_dataset_xxx.zip``)
            * ``training_data.csv``: the training data
            (``numerai_training_data.csv``)
            * ``tournament_data.csv``: the tournament data
            (``numerai_tournament_data.csv``)
            * ``example_predictions.csv``: example predictions
            (``example_predictions.csv``)

            Note that ``example_model.py`` and ``example_model.r`` are not referenced,
            as these are to no use for us.
        """
        self.apc = NumerAPI()

        current_round = self.apc.get_current_round()
        dataset_name = "numerai_dataset_{0}.zip".format(current_round)
        dataset_dir = "numerai_dataset_{0}".format(current_round)

        assert self.apc.download_current_dataset(dest_path=self.output_path,
                                                 dest_filename=dataset_name,
                                                 unzip=True)

        # see numerapi download_current_dataset
        dataset_path = os.path.join(self.output_path, dataset_dir)

        test_data_path = os.path.join(dataset_path, 'numerai_training_data.csv')
        tournament_data_path = os.path.join(dataset_path,
                                            'numerai_tournament_data.csv')
        example_data_path = os.path.join(dataset_path,
                                         'example_predictions.csv')

        out = {
            'zipfile': luigi.LocalTarget(os.path.join(self.output_path, dataset_name)),
            'training_data.csv': luigi.LocalTarget(test_data_path),
            'tournament_data.csv': luigi.LocalTarget(tournament_data_path),
            'example_predictions.csv': luigi.LocalTarget(example_data_path)
        }
        print(out)
        return out

    def run(self):
        out = self.output()

