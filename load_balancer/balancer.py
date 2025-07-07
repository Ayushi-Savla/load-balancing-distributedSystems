from flask import Flask, request, jsonify  # Flask for web server, request/jsonify for API
from flask_cors import CORS   # For enabling Cross-Origin Resource Sharing
import requests           # To forward client requests to backend server
import subprocess     # To run shell commands (for managing Docker containers)
import os
from consistent_hash import ConsistentHash


app = Flask(__name__)
CORS(app)
hash_map = ConsistentHash()
replicas = ["Server1", "Server2", "Server3"]
for r in replicas:
    hash_map.add_server(r)

@app.route('/rep', methods=['GET'])
def rep():
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than newly added instances", "status": "failure"}), 400

    for i in range(n):
        name = hostnames[i] if i < len(hostnames) else f"server_{len(replicas)+1}"
        subprocess.run(["docker", "run", "--name", name, "--network", "net1", "-e", f"SERVER_ID={name}", "-d", "server:latest"])
        hash_map.add_server(name)
        replicas.append(name)

    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def rm():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than removable instances", "status": "failure"}), 400

    targets = hostnames[:n] + replicas[:max(0, n - len(hostnames))]

    for name in targets:
        subprocess.run(["docker", "stop", name])
        subprocess.run(["docker", "rm", name])
        hash_map.remove_server(name)
        if name in replicas:
            replicas.remove(name)

    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

@app.route('/<path:endpoint>', methods=['GET'])
def forward(endpoint):
    import random
    client_id = random.randint(100000, 999999)
    server = hash_map.get_server(client_id)
    try:
        # Pick the server using consistent hash based on request path
        r = requests.get(f'http://{server}:5000/{endpoint}')
        return r.content, r.status_code
    except:
        return jsonify({"message": "<Error> Cannot reach server", "status": "failure"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
