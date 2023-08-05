from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import desc
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from utils import pretty_print_tweets, pretty_print_tweet
import os
from constants import db_user, db_pass
username = db_user
password = db_pass
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@localhost/aicomm'
db = SQLAlchemy(app)


# Model for Users
class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120))

# Model for Tweets
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.Column(db.String(80))
    message = db.Column(db.Text)
    replies = db.relationship('Reply', backref='tweet', lazy=True)

# Model for Replies
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text)
    username = db.Column(db.String(80))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)

class TweetLock(db.Model):
    tweet_id = db.Column(db.Integer, primary_key=True)
    owner_username = db.Column(db.String(80))


# Login API
@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    user = User.query.filter_by(username=login_data['username']).first()
    if user and check_password_hash(user.password, login_data['password']):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure"}), 401


@app.route('/fetch', methods=['GET'])
def fetch():
    size_limit = request.args.get('size_limit', default=10, type=int)
    tweets = Tweet.query.order_by(desc(Tweet.timestamp)).limit(size_limit).all()
    tweets_list = []
    for t in tweets:
        tweet_data = {
            "id": t.id,
            "timestamp": t.timestamp,
            "sender": t.sender,
            "message": t.message,
            "replies": [
                {
                    "reply_id": r.id,
                    "reply_timestamp": r.timestamp,
                    "reply_message": r.message,
                    "reply_username": r.username
                } for r in t.replies
            ]
        }
        tweets_list.append(tweet_data)
    return jsonify(tweets_list)

# Send new Tweet API
@app.route('/send', methods=['POST'])
def send():
    tweet_data = request.json
    if len(tweet_data['message']) > 160:
        return jsonify({"status": "failure", "reason": "Tweet exceeds 160 characters"}), 400

    new_tweet = Tweet(sender=tweet_data['sender'], message=tweet_data['message'])
    db.session.add(new_tweet)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/reply', methods=['POST'])
def reply():
    reply_data = request.json
    if len(reply_data['message']) > 140:
        return jsonify({"status": "failure", "reason": "Reply exceeds 140 characters"}), 400

    new_reply = Reply(message=reply_data['message'], username=reply_data['username'], tweet_id=reply_data['tweet_id'])
    db.session.add(new_reply)
    db.session.commit()
    print(f"For tweet id=:{reply_data['tweet_id']}")
    print(f"User: {reply_data['username']} replies: {reply_data['message']}")
    return jsonify({"status": "success"})


@app.route('/acquire_lock', methods=['POST'])
def acquire_lock():
    data = request.json
    tweet_id = data.get('tweet_id')
    username = data.get('username')

    # Check if there's already a lock for the tweet
    existing_lock = TweetLock.query.get(tweet_id)

    if existing_lock is not None:
        # If the lock already exists and is owned by this user, we can renew it
        if existing_lock.owner_username == username:
            return jsonify({"lock_acquired": True})
        # If the lock is owned by someone else, we can't acquire it
        else:
            return jsonify({"lock_acquired": False})

    # If there's no existing lock, we can create a new one
    new_lock = TweetLock(tweet_id=tweet_id, owner_username=username)
    db.session.add(new_lock)
    db.session.commit()

    return jsonify({"lock_acquired": True})


@app.route('/release_lock', methods=['POST'])
def release_lock():
    data = request.json
    tweet_id = data.get('tweet_id')
    username = data.get('username')

    # Check if there's a lock for the tweet
    existing_lock = TweetLock.query.get(tweet_id)

    if existing_lock is not None:
        # Only the user who owns the lock can release it
        if existing_lock.owner_username == username:
            db.session.delete(existing_lock)
            db.session.commit()
            return jsonify({"lock_released": True})
        # If the lock is owned by someone else, we can't release it
        else:
            return jsonify({"lock_released": False})

    # If there's no existing lock, there's nothing to release
    return jsonify({"lock_released": False})


if __name__ == '__main__':
    with app.app_context(): # This will provide the required application context
        db.create_all() # Now you can call create_all() method
    app.run(debug=True)