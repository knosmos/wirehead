from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)

COMPONENTS = []
CONTEXT = ""
BUILD_STATE = {
    "status": "idle",
    "components": {},
    "adjGraph": {},
    "layouts": {},
}

@app.route('/setquery', methods=['POST'])
def set_query():
    data = request.json
    components = data.get('components', [])
    context = data.get('context', "")
    print("Received components:", components)
    print("Received context:", context)
    return jsonify({"status": "success", "message": "Query received"}), 200

@app.route("/buildstatus", methods=['GET'])
def build_status():
    return jsonify(BUILD_STATE), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)