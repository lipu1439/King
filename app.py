from flask import Flask
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

MONGO_URI = os.getenv("mongodb+srv://lipugaming143:6Nr0esB4bjMh7buR@cluster0.vlmsl3q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['likebot']
users = db['verifications']

@app.route("/verify/<code>")
def verify(code):
    user = users.find_one({"code": code})
    if user and not user.get("verified"):
        users.update_one({"code": code}, {"$set": {"verified": True, "verified_at": datetime.utcnow()}})
        return "✅ Verification successful. Bot will now process your like."
    return "❌ Link expired or already used."

# Vercel entry point
def handler(request, response):
    return app(request.environ, response.start_response)