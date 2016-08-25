# -*- coding: utf-8 -*-
import os
from datetime import datetime
import urllib2

import luigi
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import BernoulliNB

from numerai_fetch_training_data import FetchAndExtractData


class TrainAndPredict(luigi.Task):
    """
    Trains a naïve bayes classifier with an assumed bernoulli distribution of
    the features, then predicts the targets on the tournament data.
    """
    dataset_path = luigi.Parameter(
        default='https://datasets.numer.ai/57b4899/numerai_datasets.zip')
    output_path = luigi.Parameter(default='./data/')

    def requires(self):
        return FetchAndExtractData(output_path=self.output_path,
                                   dataset_path=self.dataset_path)

    def output(self):
        req = urllib2.Request(self.dataset_path, headers={'User-Agent': "Foo"})
        res = urllib2.urlopen(req)

        # TODO: not really failure tolerant with the formatting. is it some
        # kind of standard? (which doesn't guarantee anything, of course)
        lmd = datetime.strptime(dict(res.info())['last-modified'],
                                '%a, %d %b %Y %H:%M:%S %Z')

        fn = lmd.strftime('%d_%m_%Y_Bernoulli_NB__a_0_64__bin_0_23.csv')
        return luigi.LocalTarget(os.path.join(self.output_path,
                                              fn))

    def run(self):
        data = self.input()
        out = self.output()

        test_df = pd.read_csv(data['training_data.csv'].path)
        pred_df = pd.read_csv(data['tournament_data.csv'].path)

        training_indices, testing_indices = train_test_split(
            test_df.index,
            stratify=test_df['target'].values,
            train_size=0.75,
            test_size=0.25)

        result1 = test_df.copy()

        # Perform classification with a BernoulliNB classifier
        bnb1 = BernoulliNB(alpha=0.64, binarize=0.23)
        bnb1.fit(result1.loc[training_indices].drop('target', axis=1).values,
                 result1.loc[training_indices, 'target'].values)

        # Perform prediction
        val = pred_df.drop('t_id', axis=1)
        nb = bnb1.predict_proba(val)
        pred_df['probability'] = nb[:, 1]

        pred_df.to_csv(out.path,
                       columns=('t_id', 'probability'),
                       index=None)
