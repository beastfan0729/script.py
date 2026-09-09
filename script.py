import os
import random
import yt_dlp
from googleapiclient.discovery import build

# GitHub Secrets se API Key lein
API_KEY = os.environ.get('YOUTUBE_API_KEY')

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
        videoDuration='short',  # Only YouTube Shorts
        maxResults=10
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
    """yt-dlp ka use karke video download karta hai (Bot Prevention Bypass ke saath)"""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloaded_video.mp4',
        'overwrites': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web']
            }
        }
    }
    
    print("Downloading video with yt-dlp...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    print("Video successfully downloaded as downloaded_video.mp4")

if __name__ == '__main__':
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set!")
        
    url = get_random_short(API_KEY)
    download_video(url)
