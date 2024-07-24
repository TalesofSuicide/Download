from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <html>
    <head>
        <style>
            body {
                background-image: url('https://imgs.search.brave.com/BHyziE80tXpw8mYUQKtJ0NEL_hLWWkg5DKKFk6-tUvo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzL2YzLzQ4/LzNmL2YzNDgzZjkw/ZDdlMDIxODEwMDFk/OGE2MTY2ZmI5Nzk2/LmpwZw');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            form {
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            input[type="text"] {
                width: 80%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="Enter YouTube URL">
            <button type="submit">Download</button>
        </form>
    </body>
    </html>
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
    from keepalive import keep_alive
    keep_alive()
    app.run(host='0.0.0.0', port=8080)
