from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='hotels-list', static_url_path='/hotels-list')

@app.route('/')
def home():
    return send_from_directory('hotels-list', 'index.html')

@app.route('/hotels-list/<path:filename>')
def serve_static(filename):
    return send_from_directory('hotels-list', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
