import openai
from utils import pretty_print_tweet, pretty_print_tweets
import json
import constants


openai.api_key = constants.openai_api_key




class OpenAIBot:
    def __init__(self, username, model='gpt-4'):
        self.username = username
        self.model = model

    def ask_ai(self, prompts):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=prompts,
            max_tokens=300
        )
        # print(completion)
        return (completion["choices"][0]["message"]["content"])
    def _want_to_reply(self, tweet, tweets):
        # Do not reply self
        if(len(tweet['replies']) > 0 and tweet['replies'][-1]['reply_username'] == self.username):
            # print("Do not reply self")
            return False

        # Do not reply too long conversations
        if (len(tweet['replies']) > 5):
            return False

        pretty_tweet = pretty_print_tweet(tweet)
        pretty_tweets = pretty_print_tweets(tweets)
        ask_result = self.ask_ai(constants.generate_want_to_reply_prompt(pretty_tweet, pretty_tweets, self.username))
        return 'Yes' in ask_result or 'yes' in ask_result

    def want_to_reply(self, tweets):
        for tweet in tweets:
            # print("Considering:", tweet)
            if(self._want_to_reply(tweet, tweets)):
                return tweet['id']
        return None

    def reply_tweet(self, tweet, tweets):
        pretty_tweet = pretty_print_tweet(tweet)
        pretty_tweets = pretty_print_tweets(tweets)
        reply = self.ask_ai(constants.generate_reply_prompt(pretty_tweet, pretty_tweets, self.username))
        return reply

    def _want_to_send(self, tweets):
        pretty_tweets = pretty_print_tweets(tweets)
        result = self.ask_ai(constants.generate_want_to_send_prompt(pretty_tweets, self.username))
        return 'Yes' in result or 'yes' in result

    def want_to_send(self, tweets):
        return self._want_to_send(tweets)

    def write_tweet(self, tweets):
        tweet = self.ask_ai(constants.generate_tweet_prompt(tweets, self.username))
        return tweet