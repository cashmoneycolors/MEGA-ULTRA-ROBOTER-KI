import os
from flask import Blueprint, jsonify, request

local_storage_bp = Blueprint('local_storage', __name__)
BASE_PATH = r"C:\AethelosGAZI\data"

@local_storage_bp.route('/local/list', methods=['GET'])
def list_files():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    files = os.listdir(BASE_PATH)
    return jsonify({"files": files})

@local_storage_bp.route('/local/read', methods=['POST'])
def read_file():
    filename = request.json.get('filename')
    path = os.path.join(BASE_PATH, filename)
    if not os.path.isfile(path):
        return jsonify({"error": "Datei nicht gefunden"}), 404
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return jsonify({"filename": filename, "content": content})

@local_storage_bp.route('/local/write', methods=['POST'])
def write_file():
    filename = request.json.get('filename')
    content = request.json.get('content')
    path = os.path.join(BASE_PATH, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return jsonify({"status": "ok", "filename": filename})
