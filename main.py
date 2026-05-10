import os, json, redis
from flask import Flask, request, jsonify

app = Flask(__name__)
# PASTE YOUR UPSTASH URL HERE
REDIS_URL = "rediss://default:gQAAAAAAAdOdAAIgcDFmOGJmYmYyMWY4Mjg0ZWQ3OGRmNDM5ZmQyN2Q2ZDRiZg@fun-gecko-119709.upstash.io:6379e"
r = redis.from_url(REDIS_URL)

@app.route("/vote", methods=["POST"])
def receive_vote():
    vote = request.get_json()
    if not vote or "user_id" not in vote:
        return jsonify({"error": "Invalid"}), 400
    
    # Drop vote into Redis queue
    r.lpush("vote_queue", json.dumps(vote))
    return jsonify({"status": "Vote Queued"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))