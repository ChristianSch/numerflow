# numerflow
Data workflows for the numer.ai machine learning competition

## Status
I just started to work on this, and a lot is not optimal. I'm glad if you have
any feedback, so just open up an issue (if there isn't already one). If you
have specific tasks that you want to see implemented, hit me up via the issues,
twitter or slack (@rogue).

## Tasks
Currently implemented:
* fetch and extract the datasets
* train and predict

### Planned
* automated dataviz and analysis (seaborn, nbconvert executed) in a jupyter
notebook
* automatic upload

## Documentation
### `FetchAndExtractData`
#### Parameters
* `dataset-path`: where the datasets should be saved eventually (defaults to
    `./data/`)

## Usage
Prepare the project:
```
pip install -r requirements.txt
```

To fetch the training data run
```
env PYTHONPATH='' luigi --local-scheduler --module tasks.numerai_fetch_training_data FetchAndExtractData
```
