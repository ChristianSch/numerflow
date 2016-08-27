# numerflow
Data workflows for the numer.ai machine learning competition

## Important Note
Please respect that the API of numer.ai is not officially publicized, thus
please restrain from putting too much pressure on the API and their S3 buckets.

This also means that the API can change without notice, and that this project
might fail without a warning.

## Status
I'm glad if you have any feedback, so just open up an issue (if there isn't
already one). If you have specific tasks that you want to see implemented, hit
me up via the issues, twitter or slack (@rogue).

**Update:**
(2016-08-27) I completed a fully functional (though exemplary) pipeline, which
fetches the datasets, trains a simple Naïve Bayes on the data, and submits
the predictions automatically.
Note that if the predictions for the classifier already have been uploaded,
nothing is being done.

## Tasks
Currently implemented:
* fetch and extract the datasets
* train and predict
* automatic upload

### Planned
* automated dataviz and analysis (seaborn, nbconvert executed) in a jupyter
notebook

## Documentation
### `FetchAndExtractData`
Fetches the dataset zipfile and extracts the contents to `output-path`.

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset (defaults to `https://datasets.numer.ai/57b4899/numerai_datasets.zip`)

### `TrainAndPredict`
Trains a Bernoulli Naïve Bayes classifier and predicts the targets. Output file
is saved at `output-path` with a custom, timestamped file name.

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset (defaults to `https://datasets.numer.ai/57b4899/numerai_datasets.zip`)

### `UploadPredictions`
Uploads the predictions of not already uploaded.

**Note: the actual file upload does not work yet**

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset (defaults to `https://datasets.numer.ai/57b4899/numerai_datasets.zip`)
* `usermail`: user email
* `userpass`: user password
* `filepath`: path to the file ought to be uploaded

## Usage
Prepare the project:
```
pip install -r requirements.txt
```

To run the complete pipeline:
```
env PYTHONPATH='' luigi --local-scheduler --module workflow Workflow --usermail="YOUR_MAIL" --userpass="YOUR_PASS"
```
