from flask import Flask, render_template, request, redirect, url_for, jsonify
from transcriber import get_video_urls_from_channel, download_and_transcribe
import threading

app = Flask(__name__)

# Global variable to store transcriptions
transcriptions = []

def transcribe_videos(channel_id, num_videos):
    global transcriptions
    video_urls = get_video_urls_from_channel(channel_id, num_videos)
    for url in video_urls:
        transcription = download_and_transcribe(url)
        transcriptions.append(transcription)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        channel_id = request.form['channel_id']
        num_videos = int(request.form['num_videos'])
        threading.Thread(target=transcribe_videos, args=(channel_id, num_videos)).start()
        return redirect(url_for('progress'))
    return render_template('index.html')

@app.route('/progress')
def progress():
    global transcriptions
    return jsonify(transcriptions)

if __name__ == '__main__':
    app.run(port=5003, debug=True)
