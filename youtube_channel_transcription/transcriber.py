import os
import warnings
from googleapiclient.discovery import build
from dotenv import load_dotenv
import yt_dlp
import whisper
from datetime import datetime

# Suppress specific warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Load environment variables from .env file
load_dotenv()

# YouTube Data API key
youtube_api_key = os.getenv('GOOGLE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Directory to save audio files
save_dir = "docs/youtube/"
transcription_dir = os.path.join(save_dir, "test")
os.makedirs(transcription_dir, exist_ok=True)

# Path to Netscape formatted cookies file
cookies_file = os.getenv('COOKIES_FILE')
ffmpeg_location = os.getenv('FFMPEG_LOCATION')

def get_video_urls_from_channel(channel_id, num_videos):
    video_data = []
    next_page_token = None

    while len(video_data) < num_videos:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=min(50, num_videos - len(video_data)),
            pageToken=next_page_token,
            type="video",
            order="date"  # Order by date to get the most recent videos first
        )
        response = request.execute()

        for item in response['items']:
            video_data.append({
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'publishedAt': item['snippet']['publishedAt']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # Sort videos by publication date in descending order
    video_data.sort(key=lambda x: datetime.strptime(x['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

    return [video['url'] for video in video_data[:num_videos]]

def download_and_transcribe(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': cookies_file,
        'ffmpeg_location': ffmpeg_location
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)

    transcription_file_path = os.path.join(transcription_dir, info_dict['title'] + ".txt")
    with open(transcription_file_path, "w") as f:
        f.write(result["text"])

    os.remove(audio_file_path)  # Delete the audio file after transcription

    return result["text"][:500]
