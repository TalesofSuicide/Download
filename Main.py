from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os
import tempfile

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
            background-color: #d00000;
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
            background-color: #d00000;
            text-align: center;
            line-height: 30px;
            color: white;
            border-radius: 5px;
        }
    </style>
    <form id="download-form">
        <input type="text" id="url" name="url" placeholder="Enter YouTube URL" required>
        <button type="submit">Download</button>
    </form>
    <div id="progress-container" style="display:none;">
        <div id="progress-bar">0%</div>
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
                    link.download = 'downloaded_video.mp4';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    document.getElementById('progress-container').style.display = 'none';
                    alert('Download complete!');
                } else {
                    alert('Error downloading file');
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
    url = request.form.get('url')
    if not url:
        return 'URL is required', 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            output_file = temp_file.name

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_file,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, attachment_filename='downloaded_video.mp4', mimetype='video/mp4')
        else:
            return 'File not found', 404

    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
