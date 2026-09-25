import os
import random
import sys

import yt_dlp
from googleapiclient.discovery import build

# GitHub Secrets se API Key lein
API_KEY = os.environ.get('YOUTUBE_API_KEY')
COOKIE_FILE = 'cookies.txt'


def get_random_short(api_key):
    """YouTube API se Trending Shorts/Videos dhoondta hai"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Keyword list - aap isko apne content ke hisab se change kar sakte hain
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
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"Selected Video Title: {selected_video['snippet']['title']}")
    print(f"Selected Video URL: {video_url}")
    return video_url


def download_video(video_url):
    """yt-dlp ka use karke video download karta hai."""
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

    # Pass cookies.txt if the file exists (created by GitHub Actions or a local session)
    if os.path.exists(COOKIE_FILE):
        ydl_opts['cookiefile'] = COOKIE_FILE
        print(f"Using {COOKIE_FILE} for authentication...")
    else:
        print("No cookies.txt found; YouTube may block downloads without cookies.")

    print("Downloading video with yt-dlp...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as exc:
        print(f"Video download failed for {video_url}: {exc}")
        print("This often happens when YouTube blocks automation without a valid cookie file.")
        return False

    print("Video successfully downloaded as downloaded_video.mp4")
    return True


if __name__ == '__main__':
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set!")

    try:
        url = get_random_short(API_KEY)
    except Exception as exc:
        print(f"Failed to fetch a YouTube video: {exc}")
        sys.exit(1)

    if not download_video(url):
        print("Skipping upload because the selected video could not be downloaded.")
        sys.exit(0)
