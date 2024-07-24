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
            background-color: #007BFF;
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
