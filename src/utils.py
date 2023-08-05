def pretty_print_tweet(tweet, output_to_console=False):
    output = f"Tweet by {tweet['sender']}:\n{tweet['message']}\nReplies:\n"
    for reply in tweet['replies']:
        output += f"{reply['reply_username']}: {reply['reply_message']}\n"
    output += "\n"  # Add an extra newline to separate tweets if printing multiple

    if output_to_console:
        print(output)

    return output


def pretty_print_tweets(tweets, output_to_console=False):
    output = ""
    for tweet in tweets:
        output += pretty_print_tweet(tweet)
        output += "\n"

    if output_to_console:
        print(output)

    return output

