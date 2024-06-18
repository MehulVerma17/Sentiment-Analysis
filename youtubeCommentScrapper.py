# youtubeCommentScraper.py
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual API key
API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_youtube_comments(video_id):
    """
    Fetches all comments for a given YouTube video ID.
    """
    comments = []
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100
        )
        
        # Loop until all comments are fetched
        while request:
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comments.append({'author': author, 'comment': comment})
            
            # Check if there are more comments to fetch
            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=nextPageToken
                )
            else:
                break  # No more comments to fetch
        
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    
    list_comments=[]

    for cm in comments:
        list_comments.append(cm['comment'])

    return comments,list_comments


def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    import re
    
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

