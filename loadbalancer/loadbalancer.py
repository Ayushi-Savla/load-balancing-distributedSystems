from flask import Flask, request, jsonify
import random, os, time, uuid
import docker
from hash_map import ConsistentHashRing

app = Flask(__name__)
client = docker.from_env()

hash_map = ConsistentHashRing(slots=512, replicas=9)
N = 3
virtual_nodes = 9

NETWORK = "net1"
SERVER_IMAGE = "myserver:latest"
servers = {}

def generate_server_name():
    unique_suffix = str(uuid.uuid4())[:8]
    return f"Server_{unique_suffix}"

def spawn_server(name):
    container = client.containers.run(
        SERVER_IMAGE,
        name=name,
        hostname=name,
        environment={"SERVER_ID": name},
        network=NETWORK,
        detach=True,
    )
    servers[name] = container
    hash_map.add_server(name)
    return name

def remove_server(name):
    if name in servers:
        container = servers[name]
        container.stop()
        container.remove()
        del servers[name]
        hash_map.remove_server(name)

@app.route('/rep', methods=['GET'])
def list_replicas():
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": list(servers.keys())
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get("n", 0)
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({
            "message": "<Error> Length of hostname list more than newly added instances",
            "status": "failure"
        }), 400
    added = []
    for i in range(n):
        name = hostnames[i] if i < len(hostnames) else generate_server_name()
        added.append(spawn_server(name))
    return jsonify({
        "message": {
            "N":len(servers),
            "replicas": list(servers.keys()),
        },
        "status": "successful",
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get("n", 0)
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({
            "message": "<Error> Length of hostname list more than newly removed instances",
            "status": "failure"
        }), 400
    to_remove = hostnames.copy()
    extra = [s for s in servers if s not in hostnames][:n - len(hostnames)]
    to_remove.extend(extra)

    for name in to_remove:
        remove_server(name)
    return jsonify({
        "message": {
            "N": len(servers),
            "replicas": list(servers.keys()),
        },
        "status": "successful",
    }), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    request_id = random.randint(100000, 999999)
    target = hash_map.get_server(str(request_id))

    if not target or target not in servers:
        return jsonify({
            "message": "No valid server found", "status": "failure"}), 500
    try:
        container_ip = client.containers.get(target).attrs['NetworkSettings']['Networks'][NETWORK]['IPAddress']
        import requests
        resp = requests.get(f'http://{container_ip}:5000/{path}')
        return (resp.content,resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({
            "message": f"Error routing request: {str(e)}",
            "status": "failure"
        })

def initialise():
    for i in range(N):
        spawn_server(generate_server_name())

if __name__ == '__main__':
    time.sleep(3)
    initialise()
    app.run(host='0.0.0.0', port=5000)
