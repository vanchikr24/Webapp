from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram WebApp YouTube Downloader"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return jsonify({"link": f"/get_file?filename={filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_file')
def get_file():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run(debug=True, host='0.0.0.0', port=5000)
