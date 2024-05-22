from flask import Flask, render_template, request, redirect, url_for, jsonify
from transcriber import get_video_urls_from_channel, download_and_transcribe
import threading
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_folder='static')

# Global variable to store transcriptions
transcriptions = []

def transcribe_videos(channel_id, num_videos):
    """
    Fetches video URLs from a given YouTube channel and transcribes them.
    Args:
    - channel_id: The ID of the YouTube channel.
    - num_videos: The number of videos to transcribe.
    """
    global transcriptions
    video_urls = get_video_urls_from_channel(channel_id, num_videos)  # Fetch video URLs
    for url in video_urls:
        transcription_info = download_and_transcribe(url)  # Download and transcribe each video
        transcriptions.append(transcription_info)  # Append the transcription info to the global list

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page of the web application.
    GET: Renders the index.html template.
    POST: Starts the transcription process for the provided channel ID and number of videos.
    """
    if request.method == 'POST':
        channel_id = request.form['channel_id']  # Get the channel ID from the form
        num_videos = int(request.form['num_videos'])  # Get the number of videos from the form
        # Start the transcription process in a new thread
        threading.Thread(target=transcribe_videos, args=(channel_id, num_videos)).start()
        return redirect(url_for('progress'))  # Redirect to the progress page
    return render_template('index.html')  # Render the main page template

@app.route('/progress')
def progress():
    """
    Renders the progress page and starts polling for transcription updates.
    """
    return render_template('progress.html')

@app.route('/progress_data')
def progress_data():
    """
    Returns the current progress of transcriptions as a JSON response.
    """
    global transcriptions
    return jsonify(transcriptions)  # Return the list of transcriptions as JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
# Run the Flask web server on port 5003 with debug mode enabled
