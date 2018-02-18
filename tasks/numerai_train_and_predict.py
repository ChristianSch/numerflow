# -*- coding: utf-8 -*-
import os
from datetime import datetime

from numerapi.numerapi import NumerAPI
import luigi
import pandas as pd
from sklearn import metrics, preprocessing, linear_model

from .numerai_fetch_training_data import FetchAndExtractData


class TrainAndPredict(luigi.Task):
    """
    Trains a naïve bayes classifier with an assumed bernoulli distribution of
    the features, then predicts the targets on the tournament data.
    The default signature of this task is ``TrainAndPredict(output_path='./data')``.

    :param: output_path (str):
        path to the directory where the predictions shall be saved to, defaults to
        ``./data``.
    """
    output_path = luigi.Parameter(default='./data/')

    def requires(self):
        """
        Dependencies to be fullfiled prior to execution. This task needs the
        :py:class:`tasks.numerai_fetch_training_data.FetchAndExtractData` task that provides
        the training/tournament data.
        """
        return FetchAndExtractData(output_path=self.output_path)

    def output(self):
        """
        Saves outputs of this task--which is a csv file of the predictions made for the
        given data.
        """
        self.apc = NumerAPI()
        fn ='predictions_{0}_LogisticRegression.csv'.format(self.apc.get_current_round())
        return luigi.LocalTarget(os.path.join(self.output_path, fn))

    def run(self):
        """
        Trains a model and makes predictions given the data. These are then saved
        to a csv file.
        """
        data = self.input()
        out = self.output()

        training_data = pd.read_csv(data['training_data.csv'].path, header=0)
        prediction_data = pd.read_csv(data['tournament_data.csv'].path, header=0)

        # Transform the loaded CSV data into numpy arrays
        features = [f for f in list(training_data) if "feature" in f]
        X = training_data[features]
        Y = training_data["target"]
        x_prediction = prediction_data[features]
        ids = prediction_data["id"]

        # This is your model that will learn to predict
        model = linear_model.LogisticRegression(n_jobs=-1)

        # Your model is trained on the training_data
        model.fit(X, Y)

        # Your trained model is now used to make predictions on the
        # numerai_tournament_data
        # The model returns two columns: [probability of 0, probability of 1]
        # We are just interested in the probability that the target is 1.
        y_prediction = model.predict_proba(x_prediction)
        results = y_prediction[:, 1]
        results_df = pd.DataFrame(data={'probability': results})
        joined = pd.DataFrame(ids).join(results_df)

        print("Writing predictions to predictions.csv")
        # Save the predictions out to a CSV file
        joined.to_csv("predictions.csv", index=False)
        y_prediction = model.predict_proba(x_prediction)
        results = y_prediction[:, 1]
        results_df = pd.DataFrame(data={'probability': results})
        joined = pd.DataFrame(ids).join(results_df)

        print("Writing predictions to predictions.csv")
        # Save the predictions out to a CSV file
        joined.to_csv(out.path, index=False)
