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

**Note: the actual file upload does not work yet**

#### Parameters
* `output-path`: where the datasets should be saved eventually (defaults to
    `./data/`)
* `dataset-path`: URI of the remote dataset
* `usermail`: user email
* `userpass`: user password
* `filepath`: path to the file ought to be uploaded

## API Controller Documentation
### `login`
* `user_mail`: Mail address of the user
* `user_password`: User password

If successful, the `auth_token` and `user_name` attribute of the controller
instance are filled according to the server response.

### `fetch_submissions`
* `usern`: (optional) username

If `usern` is provided, the unauthorized version of the user's submissions
are fetched. (Overwrites even authorized api controller instances.)

Otherwise, and if authorized (`auth_token` is set), the complete submissions
(includes filenames, as opposed to the unauthorized request, which does not
include filenames) for the authorized user is fetched.

If neither, `None` is returned.

### `fetch_competitions`
Fetches the data (including leaderboard) for the current and maybe upcoming
round.

### `fetch_current_competition`
Fetches the current competition data.

### `fetch_current_dataset_uri`
Fetches the URI of the dataset for the running round.

### `upload_submission`
* `file_path`: Path to the file

Authorizes the upload, uploads the file to Amazon S3 and submits the
predictions to numer.ai. Returns the updated leaderboard.


### `fetch_prediction_count`
Fetches the number of all submissions of all participants.

## Usage
Prepare the project:
```
pip install -r requirements.txt
```

To run the complete pipeline:
```
env PYTHONPATH='' luigi --local-scheduler --module workflow Workflow --usermail="YOUR_MAIL" --userpass="YOUR_PASS"
```
