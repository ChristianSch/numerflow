# numerflow
Data workflows for the numer.ai machine learning competition

## Tasks
Currently implemented:
* fetch and extract the datasets
* train and predict
* automatic upload

## Task Documentation
### `FetchAndExtractData`
Fetches the dataset zipfile and extracts the contents to `output-path`.

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset

### `TrainAndPredict`
Trains a Bernoulli Naïve Bayes classifier and predicts the targets. Output file
is saved at `output-path` with a custom, timestamped file name.

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset

### `UploadPredictions`
Uploads the predictions of not already uploaded.

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset
* `usermail`: user email
* `userpass`: user password
* `filepath`: path to the file ought to be uploaded

## Usage
Prepare the project:
```
pip install -r requirements.txt --ignore-installed
```

If not alread done create an API key [here](https://numer.ai/account) with at least the
following permissions:
* Upload submissions.
* View historical submission info.
* View user info, (e.g. balance, withdrawal history)

To run the complete pipeline:
```
env PYTHONPATH='.' luigi --local-scheduler --module workflow Workflow --secret="YOURSECRET" --public-id="YOURPUBLICID"
```
