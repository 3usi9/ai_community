import random
import time

import requests
import json
from driver import GetDriver
import constants
from utils import pretty_print_tweets, pretty_print_tweet
import threading

class CommunityClient:
    def __init__(self, client_id, driver_name):
        self.client_id = client_id
        self.username = constants.credentials[client_id]['username']
        self.password = constants.credentials[client_id]['password']
        self.base_url = 'http://127.0.0.1:5000'
        self.driver_name = driver_name
        self.driver = GetDriver(self.driver_name, self.username)

    def login(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(f'{self.base_url}/login', json=data)
        return response.json()

    fetch_backup = {}
    def fetch(self):
        response = requests.get(f'{self.base_url}/fetch')
        fetchs = response.json()
        if(fetchs == self.fetch_backup):
            return {} # Not changed
        self.fetch_backup = fetchs
        return fetchs

    def send(self, tweet):
        data = {
            'sender': self.username,
            'message': tweet
        }
        response = requests.post(f'{self.base_url}/send', json=data)
        return response.json()

    def reply(self, tweet_id, reply):
        data = {
            'message': reply,
            'username': self.username,
            'tweet_id': tweet_id
        }
        response = requests.post(f'{self.base_url}/reply', json=data)
        return response.json()
    def acquire_lock(self, tweet_id):
        data = {
            'username': self.username,
            'tweet_id': tweet_id
        }
        response = requests.post(f'{self.base_url}/acquire_lock', json=data)
        return response.json()['lock_acquired']

    def release_lock(self, tweet_id):
        data = {
            'username': self.username,
            'tweet_id': tweet_id
        }
        response = requests.post(f'{self.base_url}/release_lock', json=data)
        return response.json()['lock_released']

    def work_loop(self):
        while True:
            time.sleep(random.randint(1, 5))
            tweets = self.fetch()
            # reply
            reply_tweet_id = self.driver.want_to_reply(tweets)
            if (reply_tweet_id is not None):
                if not self.acquire_lock(reply_tweet_id):
                    print(f"[User {self.username}] lock not acquired for tweet: {reply_tweet_id}")
                    continue
                reply_tweet = {}
                for tweet in tweets:
                    if (tweet['id'] == reply_tweet_id):
                        reply_tweet = tweet
                        break
                if (reply_tweet == {}):
                    self.release_lock(reply_tweet_id)  # Release lock in case of failure
                    raise AssertionError("Reply tweet not found.")

                msg = self.driver.reply_tweet(tweet=reply_tweet, tweets=tweets)
                print(f"[User {self.username}] try to reply to tweet: {pretty_print_tweet(reply_tweet)}")
                print(f"[User {self.username}] The reply message is: {msg}")
                self.reply(reply_tweet['id'], msg)

                self.release_lock(reply_tweet_id)  # Release lock after replying
                time.sleep(10 + random.randint(1,10))
                continue

            # send
            if (self.driver.want_to_send(tweets)):
                msg = self.driver.write_tweet(tweets)
                print(f"[User {self.username}] try to send a new tweet: {msg}")
                self.send(msg)
                time.sleep(10+ random.randint(1,10))
                continue
            time.sleep(5+ random.randint(1,10))


def main():
    # Number of clients
    num_clients = constants.num_clients

    # List to hold the threads
    threads = []

    for i in range(num_clients):
        # Create a client
        client = CommunityClient(client_id=i, driver_name='gpt-3.5-turbo')

        # Create a thread that calls the client's work_loop method
        thread = threading.Thread(target=client.work_loop)

        # Add the thread to the list of threads
        threads.append(thread)

        # Start the thread
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()


# the client should:
# 1. load driver
#     driver = chat_driver('gpt-4')
# 2. fetch current tweets
#     tweets = fetch()
# 3. if(event): try_to_reply_tweet()
# 4. if(event): try_to_publish_tweet()
