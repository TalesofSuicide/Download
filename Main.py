from flask import Flask, request, send_file, render_template_string
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
    </style>
    <form action="/download" method="post">
        <input type="text" name="url" placeholder="Enter YouTube URL">
        <button type="submit">Download</button>
    </form>
    ''')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'outtmpl': 'downloaded_video.%(ext)s',
        'format': 'best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info_dict)

    return send_file(video_file, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
