Targets
-------

.. currentmodule:: targets

Targets are products of Luigi tasks. These targets are checked for existance prior to
running a tasks. This task is only run if any of the targets does not exist. A task also
cannot exit with success when the target isn't created after the task was run.

.. autoclass:: targets.numerai_submission.SubmissionTarget
    :members:

    .. automethod:: __init__
