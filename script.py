import os
import random
import sys
import yt_dlp
from googleapiclient.discovery import build

API_KEY = os.environ.get('YOUTUBE_API_KEY')
COOKIE_FILE = 'cookies.txt'


def get_random_short(api_key):
    """Fetches a trending short video using YouTube API."""
    youtube = build('youtube', 'v3', developerKey=api_key)

    search_queries = ['#shorts', 'viral shorts', 'trending shorts', 'funny shorts']
    query = random.choice(search_queries)

    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        videoDuration='short',
        maxResults=10,
        regionCode='US',
        relevanceLanguage='en'
    )
    response = request.execute()

    items = response.get('items', [])
    if not items:
        raise Exception("No videos found from API search.")

    selected_video = random.choice(items)
    video_id = selected_video['id']['videoId']
    
    print(f"Selected Video Title: {selected_video['snippet']['title']}")
    return f"https://www.youtube.com/watch?v={video_id}"


def download_video(video_url):
    """Downloads video using yt-dlp with cookie support and fallback options."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best[ext=mp4]/best',
        'outtmpl': 'downloaded_video.mp4',
        'overwrites': True,
        'noplaylist': True,
        'no_warnings': True,
        'geo_bypass': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'tv_embedded', 'mweb', 'web_creator']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36'
        }
    }

    if os.path.exists(COOKIE_FILE):
        ydl_opts['cookiefile'] = COOKIE_FILE
        print(f"Using {COOKIE_FILE} for authentication...")

    print(f"Downloading video from {video_url} with yt-dlp...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as exc:
        print(f"Video download failed: {exc}")
        return False

    print("Video successfully downloaded as downloaded_video.mp4")
    return True


if __name__ == '__main__':
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set!")
    
    try:
        url = get_random_short(API_KEY)
    except Exception as exc:
        print(f"Failed to fetch video details: {exc}")
        sys.exit(1)

    if not download_video(url):
        print("Skipping download task because YouTube blocked the video request.")
        sys.exit(0)
