import json, redis, os, threading
from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

# --- CONFIGURATION ---
REDIS_URL = "rediss://default:gQAAAAAAAdOdAAIgcDFmOGJmYmYyMWY4Mjg0ZWQ3OGRmNDM5ZmQyN2Q2ZDRiZg@fun-gecko-119709.upstash.io:6379"
# Cleaned URL: No brackets, no double quotes
MONGO_URL = "mongodb+srv://suprcharlsge:yG02vFqiiXNNoLIy@cluster0.smczchr.mongodb.net/?appName=Cluster0"

@app.route('/')
def health_check():
    return "Worker is running! I am watching the queue.", 200

def run_worker():
    print("Chef is entering the kitchen...")
    try:
        r = redis.from_url(REDIS_URL)
        mongo_client = MongoClient(MONGO_URL)
        db = mongo_client.voting_db
        print("Connected to Redis and MongoDB. Waiting for votes...")
        
        while True:
            # This waits for a message from the "bucket"
            _, message = r.brpop("vote_queue")
            vote = json.loads(message)
            
            # Idempotency: prevent double-saving
            vote["_id"] = f"{vote['user_id']}_{vote['poll_id']}"
            
            try:
                db.votes.insert_one(vote)
                print(f"SUCCESS: Saved vote {vote['_id']}")
            except Exception as e:
                print("Duplicate vote ignored.")
    except Exception as e:
        print(f"CRITICAL ERROR in Worker: {e}")

# START THE WORKER IMMEDIATELY
# This runs in the background the moment Render loads the file
threading.Thread(target=run_worker, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
