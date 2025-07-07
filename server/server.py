from flask import Flask, jsonify        # Flask for creating the web server, jsonify to format responses
import os                               # For accessing environment variables


app = Flask(__name__)
server_id = os.environ.get("SERVER_ID", "Unknown")

@app.route('/home', methods=['GET'])
def home():
    return jsonify({
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    }), 200     # HTTP status code 200 (OK)

# Define the '/heartbeat' endpoint used by the load balancer to check if this server is alive
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200
# Start the Flask app on host 0.0.0.0 so it is accessible from outside the container
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
