import logging
import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from api import api

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

app.register_blueprint(api, url_prefix='/api')


@app.before_request
def log_request_info():
    app.logger.info("%s %s", request.method, request.path)


@app.after_request
def log_response_info(response):
    app.logger.info("%s %s -> %s", request.method, request.path, response.status)
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    file_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(file_path):
        if os.path.isdir(file_path):
            return send_from_directory(file_path, 'index.html')
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3001)  # Match the frontend port
