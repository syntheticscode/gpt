import tweepy
import key
import gpt_api
from time import sleep
from typing import List
import sys
import json

answer_format = ["tweet number 1", "tweet number 2", "tweet number 3"]


def send_tweet(status: str, previous_tweet_id: int = None) -> int:
    if not status:
        print("No status to tweet")
        return None
    auth = tweepy.OAuth1UserHandler(
        key.TWITTER_SYNTHETICS_CONSUMER_KEY,
        key.TWITTER_SYNTHETICS_CONSUMER_SECRET,
        key.TWITTER_SYNTHETICS_BASE_APP_ACCESS_TOKEN,
        key.TWITTER_SYNTHETICS_BASE_APP_ACCESS_SECRET,
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        response = api.update_status(status, in_reply_to_status_id=previous_tweet_id)
    except tweepy.TweepyException as e:
        print(e)
        return None
    print("Tweet sent:", response.id)
    return response.id


# write a function that takes a list of statuses and tweets them
def send_tweets(statuses: list) -> List[str]:
    tweet_ids = []
    for status in statuses:
        tweet_id = send_tweet(status, tweet_ids[-1] if tweet_ids else None)
        if not tweet_id:
            print("Tweet failed, aborting")
            return tweet_ids
        tweet_ids.append(tweet_id)
        sleep(1)
    return tweet_ids


# given a topic return a list of tweets using gpt_api
def generate_tweet_statuses(topic: str, num=1):
    prompt = f"Respond with exactly {num} tweets about: {topic}. NO EMOJIS. Remeber to add hashtags and to repy only with a json in this format:\n\n{json.dumps(answer_format)}"
    all_tweet = json.loads(gpt_api.respond(prompt))
    return [tweet.strip() for tweet in all_tweet if tweet][:num]


# generate a list of tweets given a topic, select the one we like, and send it.
# tweetid is the id of the tweet we are replying to (if any)
def generate_select_and_send_one(topic: str, num = 3, tweet_id = None):
    print(f"Generating tweets for topic: `{topic}`")
    tweets = generate_tweet_statuses(topic, num)
    for i, tweet in enumerate(tweets):
        print(f"Tweet {i+1}: `{tweet}`")
    selected_tweet = int(input("Select a tweet to send, 0 for more options: "))
    if selected_tweet == 0:
        generate_select_and_send_one(topic, num)
        return
    print("Sending tweet:", tweets[selected_tweet - 1])
    return send_tweet(tweets[selected_tweet - 1], tweet_id)


# generate a list of tweets given a topic, and send them
def generate_and_send_tweets(topic: str, num):
    tweets = generate_tweet_statuses(topic, num)
    for i, tweet in enumerate(tweets):
        print(f"Tweet {i+1}: `{tweet}`")
    send_tweets(tweets)


# write a function that takes a topic and tweets about it
if __name__ == "__main__":
    # default topic
    topic = "python, ai, twitter and chat gpt projects, Using AI for coding and automating away real-world"
    topic = "the stream about sending twwets with gpt3 is over, here is the link https://www.twitch.tv/videos/1696211036 , use also #ChatGpt as hashtag"
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    generate_select_and_send_one(topic, 5, 1610169292535828480)

"""
example output:
Generating tweets for topic: python and chat gpt projects, Using AI for coding and automating away real-world
Tweet 1: #Python and #ChatGPT projects are using #AI for coding and automating away real-world tasks. It's an exciting time to be an AI developer! #AI #Coding #Automation
Tweet 2: The possibilities of #AI are endless! #Python and #ChatGPT projects are enabling developers to automate away real-world tasks. #Coding #Automation
Tweet 3: Developers are leveraging #AI to create #Python and #ChatGPT projects that automate away real-world tasks. The future of AI is here! #Coding #Automation
Select a tweet to send, 0 for more options: 3
Sending tweet: Developers are leveraging #AI to create #Python and #ChatGPT projects that automate away real-world tasks. The future of AI is here! #Coding #Automation
"""
