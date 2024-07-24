from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <style>
        body {
            background-image: url('https://imgs.search.brave.com/BHyziE80tXpw8mYUQKtJ0NEL_hLWWkg5DKKFk6-tUvo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzL2YzLzQ4/LzNmL2YzNDgzZjkw/ZDdlMDIxODEwMDFk/OGE2MTY2ZmI5Nzk2/LmpwZw');
            background-size: cover;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        form {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
        }
        input {
            padding: 10px;
            margin-right: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        #progress-container {
            margin-top: 20px;
        }
        #progress-bar {
            width: 0;
            height: 30px;
            background-color: #8B0000; /* Dark Red Color */
            text-align: center;
            line-height: 30px;
            color: white;
            border-radius: 5px;
        }
        #status-message {
            margin-top: 10px;
            font-weight: bold;
        }
        .info-text {
            font-size: 16px;
            margin-bottom: 20px;
        }
    </style>
    <div class="info-text">
        <p>Acceptable links:</p>
        <ul>
            <li>YouTube URLs (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)</li>
            <li>Instagram URLs (e.g., https://www.instagram.com/p/your-post-id/)</li>
            <li>TikTok URLs (e.g., https://www.tiktok.com/@username/video/your-video-id)</li>
            <li>Twitter URLs (e.g., https://twitter.com/username/status/your-tweet-id)</li>
        </ul>
    </div>
    <form id="download-form">
        <input type="text" id="url" name="url" placeholder="Enter URL" required>
        <button type="submit">Download</button>
    </form>
    <div id="progress-container" style="display:none;">
        <div id="progress-bar">0%</div>
        <div id="status-message"></div>
    </div>
    <script>
        document.getElementById('download-form').onsubmit = function(event) {
            event.preventDefault();
            var url = document.getElementById('url').value;
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/download', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.responseType = 'blob';
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var link = document.createElement('a');
                    link.href = URL.createObjectURL(xhr.response);
                    link.download = 'Kurumi\'sVideo.mp4';
                    link.click();
                    document.getElementById('progress-container').style.display = 'none';
                }
            };
            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    var percentComplete = (event.loaded / event.total) * 100;
                    document.getElementById('progress-bar').style.width = percentComplete + '%';
                    document.getElementById('progress-bar').textContent = Math.round(percentComplete) + '%';
                    document.getElementById('progress-container').style.display = 'block';
                }
            };
            xhr.send('url=' + encodeURIComponent(url));
        };
    </script>
    ''')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    file_path = '/tmp/Kurumi\'sVideo.mp4'

    def download_video():
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': file_path,
            'progress_hooks': [hook],
            'noplaylist': True,  # Avoid downloading playlists
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def hook(d):
        if d['status'] == 'finished':
            print("Download finished, sending file.")
    
    # Create a separate thread for the download
    thread = Thread(target=download_video)
    thread.start()
    
    # Wait for the download to complete
    thread.join()

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, attachment_filename="Kurumi'sVideo.mp4")
    else:
        return 'Error: File not found.', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
