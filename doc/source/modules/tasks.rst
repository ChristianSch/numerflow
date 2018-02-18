Tasks
-----

.. currentmodule:: tasks

The following tasks allow for a complete workflow to be implemented from fetching the
tournament data automatically, to training a model and then submitting it.
A Luigi task is made to be used in conjunction with other tasks. Hence, dependencies
between the tasks are explicitly modeled. The functions ``requires``, which expresses
any incoming dependencies, as well as ``outputs``, which models products of a tasks, are
used for this. The ``run`` function is called, when the ``outputs`` are not yet satisfied
in order to produce the outputs. If the outputs on the other hand are already produced,
the tasks won't be run as the targets are already there.


.. autoclass:: tasks.numerai_fetch_training_data.FetchAndExtractData
    :members:

    .. automethod:: output, run

.. autoclass:: tasks.numerai_train_and_predict.TrainAndPredict
    :members:

    .. automethod:: output, run, requires


.. autoclass:: tasks.numerai_upload_predictions.UploadPredictions
    :members:

    .. automethod:: output, run
