import os
import googleapiclient.discovery
import googleapiclient.errors
from yt_dlp import YoutubeDL

# 1. Download YouTube Short Video
def download_short(video_url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios']
            }
        }
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return 'downloaded_video.mp4'

# 2. Upload to YouTube Channel
def upload_to_youtube(video_file, title):
    api_service_name = "youtube"
    api_version = "v3"
    
    # YouTube API Client Setup
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=os.environ.get("YOUTUBE_API_KEY")
    )

    request_body = {
        'snippet': {
            'title': title,
            'description': 'Auto-uploaded YouTube Short #shorts',
            'tags': ['shorts', 'mrbeast'],
            'categoryId': '24'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        }
    }

    # Execute Upload
    media_file = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = request.execute()
    print("Uploaded successfully! Video ID:", response.get("id"))

if __name__ == "__main__":
    # Top video link from Sheet
    video_url = "https://www.youtube.com/shorts/YlvcFJOE-OE"
    title = "Giving iPhones Instead Of Candy on Halloween #shorts"
    
    video_file = download_short(video_url)
    upload_to_youtube(video_file, title)
