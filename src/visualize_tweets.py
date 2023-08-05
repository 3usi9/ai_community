from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def show_tweets():
    # Make a request to your existing API to fetch the tweets
    response = requests.get('http://127.0.0.1:5000/fetch', params={'size_limit': 100})
    tweets = response.json()

    # Pass the tweets to the HTML template
    return render_template('tweets.html', tweets=tweets)

if __name__ == '__main__':
    app.run(port=5001, debug=True)