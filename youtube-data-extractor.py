# Import libraries
import os
import argparse
import pandas as pd
from datetime import datetime
from apiclient.discovery import build

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--query", "-q", help="Set a search query", default="#endsars")
parser.add_argument("--results", "-r", help="Set the number of videos to search for. \
                                            Should be between 0 and 50", default=10)
parser.add_argument("--duration", "-d", help="Set a duration for videos being searched for", \
                                        default="medium", choices=['any', 'short', 'medium', 'long'])
parser.add_argument("--date", "-d", help="Date after wihich videos should be retrieved", default="2020")

# Read arguments from the command line
args = parser.parse_args()

# Store argument values in variables for use
query = args.query
results = args.results
duration = args.duration
date = arge.date

# Youtube API KEY
API_KEY = "ENTER_YOUR_YOUTUBE_DATA_V3_API_KEY"

# Connect to the Youtube Data API with your API_KEY
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Search for results based on a query (default query is '#endsars')
# maximum allowed results = 50, default = 10
def search(query, results, duration, date):
    request = youtube.search().list(
        part = 'snippet',
        q = query,
        videoDuration = duration,
        type = 'video',
        maxResults = results,
        publishedAfter = pd.to_datetime(date).strftime('%Y-%m-%dT%H:%M:%SZ')
    )
    return request.execute()

# Create dataframe from search results
def create_search_df(query, results, duration, date):
    data = []

    for item in search(query, results, duration, date)['items']:
        row = {
            'id': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'time_published': item['snippet']['publishedAt'],
            'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
            'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }

        data.append(row)

    df = pd.DataFrame(data)
    df['time_published'] = pd.to_datetime(df['time_published']).dt.time

    return df

# Fetch video stats from youtube
def video_stats(video_id):
    request = youtube.videos().list(part='statistics', id=video_id).execute()
    stats = request['items'][0]
    return stats

# Create dataframe with video stats
def create_stats_df(stats):
    df = pd.json_normalize(stats)
    df = df[['id', 'statistics.viewCount', 'statistics.commentCount', 'statistics.likeCount',
                     'statistics.dislikeCount']]
    df.rename(columns = {'statistics.viewCount': 'views',
                         'statistics.commentCount': 'comments',
                         'statistics.likeCount': 'likes',
                         'statistics.dislikeCount': 'dislikes'}, inplace=True)
    return df

# Create final dataframe
def final_df(search_df, stats_df):
    df = search_df.merge(stats_df, how='inner', on='id')
    return df

# Save the results to a csv
def save(df):
    current_date = pd.to_datetime('now').strftime('%Y-%m-%d %H.%M.%S')
    filename = f"{current_date}_youtube_data.csv"
    df.to_csv(filename, index=False)
    print(f'File saved to {os.getcwd()}/{filename}')



def main():
    # Run functions to search youtube and extract the results to a .csv file
    search_df = create_search_df(query, results, duration)
    stats = search_df['id'].apply(video_stats)
    stats_df = create_stats_df(stats)
    df = final_df(search_df, stats_df)
    save(df)

if __name__ == '__main__':
    main()
