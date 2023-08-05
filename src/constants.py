import json

with open('config.json') as f:
    config = json.load(f)

openai_api_key = config['openai_api_key']
credentials = config['credentials']
db_user = config['database']['username']
db_pass = config['database']['password']
num_clients = len(credentials)
system_prompt = """
You are a twitter user, you can read or write twitters.
"""
chinese_prompt = "You should write new tweets or write replies using Chinese."
system_prompt += chinese_prompt
_TWEET_LENGTH_LIMIT = 3000

def generate_want_to_reply_prompt(tweet, tweets, username):
    want_to_reply_prompt = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "Current Tweets are:" + str(tweets)[:_TWEET_LENGTH_LIMIT]
        },
        {
            "role": "user",
            "content": "The tweet you may want to reply is:" + str(tweet)
        },
        {
            "role": "user",
            "content": f"You are {username}, if you are willing to reply this tweet, please output 'Yes', otherwise, please output 'No'."
        }]
    return want_to_reply_prompt

def generate_reply_prompt(tweet, tweets, username):
    reply_prompt = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "Current Tweets are:" + str(tweets)[:_TWEET_LENGTH_LIMIT]
        },
        {
            "role": "user",
            "content": "The tweet to reply is:" + str(tweet)
        },
        {
            "role": "user",
            "content": f"You are {username}, please write a reply comment, reply should not exceed 140 characters."
        },
        {
            "role": "user",
            "content": "Reply:"
        }]
    return reply_prompt

def generate_want_to_send_prompt(tweets, username):
    want_to_send_prompt = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "Current Tweets are:" + str(tweets)[:_TWEET_LENGTH_LIMIT]
        },
        {
            "role": "user",
            "content": f"You are {username}, if you want to send a new tweet, please output 'Yes', otherwise, please output 'No'."
        }]
    return want_to_send_prompt


def generate_tweet_prompt(tweets, username):
    tweet_prompt = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "Current Tweets are:" + str(tweets)[:_TWEET_LENGTH_LIMIT]
        },
        {
            "role": "user",
            "content": f"You are {username}, please write a new tweet, you can expreess your motion, bad things or good things happened recently, or something else, a tweet should not exceed 160 characters."
        },
        {
            "role": "user",
            "content": "Tweet:"
        }]

    return tweet_prompt
