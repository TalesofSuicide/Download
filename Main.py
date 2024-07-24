from flask import Flask, render_template_string, request, send_file, jsonify
import yt_dlp
import os

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
    </style>
    <form id="download-form">
        <input type="text" id="url" name="url" placeholder="Enter YouTube URL" required>
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
            xhr.responseType = 'json';
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var downloadUrl = xhr.response.url;
                    var link = document.createElement('a');
                    link.href = downloadUrl;
                    link.download = 'downloaded_video.mp4';
                    link.click();
                    document.getElementById('progress-container').style.display = 'none';
                } else {
                    alert('Error downloading file: ' + xhr.response.error);
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
    temp_path = '/tmp/downloaded_video'
    temp_file = temp_path + '.temp.mp4'

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': temp_file,
            'merge_output_format': 'mp4',  # Ensure merging to MP4
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        final_file = temp_path + '.mp4'
        if os.path.exists(temp_file):
            os.rename(temp_file, final_file)
        else:
            return jsonify({'error': 'File not found after download'}), 404

        if os.path.exists(final_file):
            return jsonify({'url': '/serve_file'})
        else:
            return jsonify({'error': 'File not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/serve_file')
def serve_file():
    file_path = '/tmp/downloaded_video.mp4'
    if not os.path.exists(file_path):
        return 'File not found', 404
    return send_file(file_path, as_attachment=True, attachment_filename='downloaded_video.mp4', mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
