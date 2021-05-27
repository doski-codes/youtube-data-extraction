# YouTube Data Extractor

## 1. Introduction

Using a Python script to extract data from YouTube using the YouTube Data API V3
and extract the results to a .csv file.

To use the script, you'll require access to the YouTube API. Go to
[YouTube Data API](https://developers.google.com/youtube/v3/getting-started) and follow the
steps to enable you access the Data API with your own `API_KEY`

## 2. Environment

To install the packages used in this project and you would require `conda` (miniconda or anaconda).

After cloning the repository run the following commands:


`cd youtube-data-extractor`

then

`conda env create -f environment.yml`

Now run the command `conda activate youtube-data-env` to activate the conda environment
with the required packages.

You can run `conda deactivate` to deactivate the environment.

## 3. Execution

After activating the environment, run `python youtube-data-extractor.py` to run the
script with it's default values.

You can specify your arguments for the search by using one of the following methods:

`python youtube-data-extractor.py -q fraud -r 20 -t long -d 2021`

or

`python youtube-data-extractor.py --query fraud --results 20 --duration long --date 2021`


### Arguments

`-q, --query` : Specify the search query. The default value is _'#endsars'_.

`-r, --results`: Specify how many items to include the search results. The allowed input
should be an integer from _0 to 50_. The default value is _10_.

`-t, --duration`: Specify how long the videos from the search results should be.

Options:
- any: Any video length.
- short: Videos length between 0 and 4 minutes.
- medium: Video length between 4 and 20 minutes (inclusive).
- long: Video length greater than 20 minutes.

The default value is _medium_.

`-d, --date`: Specify a date to filter the search results from. The default value is
_01-01-2020_.
