.. numerflow documentation master file, created by
   sphinx-quickstart on Sun Feb 18 13:50:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to numerflow's documentation!
=====================================

.. module:: numerflow

This project provides fully automated data workflows for the numer.ai machine learning
competition. The following tasks are currently implemented:

* fetch and extract the datasets
* train and predict
* automatic upload

... as well as a *task* (:py:mod:`workflow`) that implements a pipeline from fetching the training data,
to training the model and finally submitting the predictions.


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    modules/tasks.rst
    modules/targets.rst
    workflow.rst


Getting Started
---------------
Fetch the latest release from GitHub. Install the dependencies via ``pip install -r
requirements.txt``. You also need to create API credentials on the numer.ai website under
the link *account*. The following permissions are needed:

* Upload submissions.
* View historical submission info.
* View user info, (e.g. balance, withdrawal history)

You can run the example pipeline called ``Workflow`` directly::

    env PYTHONPATH='.' luigi --local-scheduler --module workflow Workflow --secret="YOURSECRET" --public-id="YOURPUBLICID"


This should fetch the most recent data, train a ``LogisticRegression`` model and submit
the predictions.
When you want to roll your own model and preprocessing, start with
:py:class:`tasks.numerai_train_and_predict.TrainAndPredict`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
