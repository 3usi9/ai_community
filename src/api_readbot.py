from utils import pretty_print_tweet, pretty_print_tweets
class ReadBot:
    def __init__(self, username):
        self.username = username

    def _want_to_reply(self, tweets):
        print(f"[{self.username}][Want To Reply Check]")
        pretty_print_tweets(tweets)
        return True

    def want_to_reply(self, tweets):
        if (self._want_to_reply(tweets)):
            return True
        return False

    def reply_tweet(self, tweet):
        print(f"[{self.username}][Reply Tweet]")
        pretty_print_tweet(tweet)
        return "hellllllo"

    def _want_to_send(self, tweets):
        print(f"[{self.username}][Want To Send Check]")
        pretty_print_tweets(tweets)
        return True
    def want_to_send(self, tweets):
        if(self._want_to_send(tweets)):
            return True
        return False

    def write_tweet(self, tweets):
        print(f"[{self.username}][Write Tweet]")
        pretty_print_tweets(tweets)
        return "This is a new tweet"
