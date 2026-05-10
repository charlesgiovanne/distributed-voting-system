import json, redis, os, threading
from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Worker is running!", 200

def run_worker():
    REDIS_URL = ""rediss://default:gQAAAAAAAdOdAAIgcDFmOGJmYmYyMWY4Mjg0ZWQ3OGRmNDM5ZmQyN2Q2ZDRiZg@fun-gecko-119709.upstash.io:6379""
    MONGO_URL = "mongodb+srv://charliesorongon_db_user:<ZizvUiwX06VO0WsO>@cluster0.xwzi76o.mongodb.net/?appName=Cluster0"
    
    r = redis.from_url(REDIS_URL)
    mongo_client = MongoClient(MONGO_URL)
    db = mongo_client.voting_db
    
    print("Chef is in the kitchen (Worker started)...")
    while True:
        _, message = r.brpop("vote_queue")
        vote = json.loads(message)
        vote["_id"] = f"{vote['user_id']}_{vote['poll_id']}"
        try:
            db.votes.insert_one(vote)
            print(f"Recorded vote: {vote['_id']}")
        except:
            print("Duplicate ignored.")

if __name__ == "__main__":
    # Start the worker logic in the background
    threading.Thread(target=run_worker, daemon=True).start()
    # Start the fake web server so Render sees it as "Active"
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
