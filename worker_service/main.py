import json, redis
from pymongo import MongoClient

# PASTE YOUR URLS HERE
REDIS_URL = "rediss://default:gQAAAAAAAdOdAAIgcDFmOGJmYmYyMWY4Mjg0ZWQ3OGRmNDM5ZmQyN2Q2ZDRiZg@fun-gecko-119709.upstash.io:6379eere"
MONGO_URL = "mongodb+srv://charliesorongon_db_user:<ZizvUiwX06VO0WsO>@cluster0.xwzi76o.mongodb.net/?appName=Cluster0"

r = redis.from_url(REDIS_URL)
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.voting_db

print("Worker is waiting for votes...")
while True:
    # Pop vote from Redis (Blocking wait)
    _, message = r.brpop("vote_queue")
    vote = json.loads(message)
    
    # IDEMPOTENCY: Use user_id + poll_id as the unique ID
    vote["_id"] = f"{vote['user_id']}_{vote['poll_id']}"
    
    try:
        db.votes.insert_one(vote)
        print(f"Recorded vote: {vote['_id']}")
    except:
        print("Duplicate vote ignored - System is Idempotent!")