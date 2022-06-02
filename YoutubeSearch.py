import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
DEVELOPER_KEY = os.getenv('YOUTUBE_API')  # YouTube API
YOUTUBE_API_SERVICE_NAME = "youtube"  # YouTube API Service Name
YOUTUBE_API_VERSION = "v3"  # YouTube API Version
# Creating Youtube resource object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def yquery(qtype, query):
    # Calling the search.list method to retreive youtube search results
    search_keyword = youtube_object.search().list(q=query, part="id, snippet", maxResults=5).execute()
    # Extracting the results from the search response
    results = search_keyword.get("items", [])

    # Empty list to store video, channel, playlist metadata
    videos = []
    playlists = []
    channels = []

    # Extracting required info from each result object
    for result in results:
        # Video result object
        if result['id']['kind'] == "youtube#video":
            videos.append("%s (%s) (%s) (%s)" % (result["snippet"]["title"],
                                                 result["id"]["videoId"], result['snippet']['description'],
                                                 result['snippet']['thumbnails']['default']['url']))
        elif result['id']['kind'] == "youtube#playlist":
            playlists.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],
                                                        result["id"]["playlistId"], result['snippet']['description'],
                                                        result['snippet']['thumbnails']['default']['url']))
        elif result['id']['kind'] == "youtube#channel":
            channels.append("% s (% s) (% s) (% s)" % (result["snippet"]["title"],
                                                       result["id"]["channelId"], result['snippet']['description'],
                                                       result['snippet']['thumbnails']['default']['url']))
    if qtype == "video":
        return videos
    elif qtype == "playlists":
        return playlists
    elif qtype == "channels":
        return channels


