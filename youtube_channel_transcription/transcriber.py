import os
import warnings
from googleapiclient.discovery import build
from dotenv import load_dotenv
import yt_dlp
import whisper
from datetime import datetime

# Suppress specific warnings about FP16 not being supported on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
youtube_api_key = os.getenv('GOOGLE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize YouTube API client using the provided API key
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Directories to save audio files and transcriptions
save_dir = "/Users/wyliebrown/training_data/dataiku"
transcription_dir = os.path.join(save_dir, "youtube")
os.makedirs(transcription_dir, exist_ok=True)  # Create directories if they don't exist

# Path to Netscape formatted cookies file and ffmpeg location from environment variables
cookies_file = os.getenv('COOKIES_FILE')
ffmpeg_location = os.getenv('FFMPEG_LOCATION')

def get_video_urls_from_channel(channel_id, num_videos):
    """
    Retrieves the most recent video URLs from a YouTube channel.

    Args:
    - channel_id: The ID of the YouTube channel.
    - num_videos: The number of video URLs to retrieve.

    Returns:
    - A list of video URLs.
    """
    video_data = []
    next_page_token = None

    while len(video_data) < num_videos:
        # Request video details from the YouTube channel
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=min(50, num_videos - len(video_data)),  # Limit results to avoid exceeding the num_videos
            pageToken=next_page_token,
            type="video",
            order="date"  # Order videos by date to get the most recent ones first
        )
        response = request.execute()

        for item in response['items']:
            video_data.append({
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'publishedAt': item['snippet']['publishedAt']
            })

        next_page_token = response.get('nextPageToken')  # Get the next page token, if available
        if not next_page_token:
            break  # Exit loop if no more pages are available

    # Sort videos by publication date in descending order
    video_data.sort(key=lambda x: datetime.strptime(x['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

    # Return the URLs of the videos
    return [video['url'] for video in video_data[:num_videos]]

def download_and_transcribe(url):
    """
    Downloads the audio from a YouTube video and transcribes it.

    Args:
    - url: The URL of the YouTube video.

    Returns:
    - A dictionary with detailed transcription information.
    """
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best quality audio
        'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),  # Save path template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': cookies_file,  # Use cookies to handle age-restricted content
        'ffmpeg_location': ffmpeg_location  # Specify the path to ffmpeg
    }

    # Download audio using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)  # Extract video info and download
        audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')  # Get the path to the downloaded audio file

    # Debug: Print the audio file path to confirm it exists
    print(f"Audio file path: {audio_file_path}")
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
        return {
            "url": url,
            "destination": audio_file_path,
            "file_name": "N/A",
            "sample_text": "Error: Audio file not found"
        }

    # Initialize Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio file
    result = model.transcribe(audio_file_path)

    # Save the transcription to a text file
    transcription_file_path = os.path.join(transcription_dir, info_dict['title'] + ".txt")
    with open(transcription_file_path, "w") as f:
        f.write(result["text"])

    # Print the path where the transcription is saved
    print(f"Transcription file saved at: {transcription_file_path}")

    # Delete the audio file after transcription
    os.remove(audio_file_path)

    # Return detailed transcription information
    return {
        "url": url,
        "destination": audio_file_path,
        "file_name": os.path.basename(transcription_file_path),
        "sample_text": result["text"][:50]
    }

