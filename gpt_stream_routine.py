"""
# send a tweet for the start of the stream
# set the twitch stream topic
# stream
# tweet end of stream with link
# generate medium article
# tweet it
"""

from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import key
import asyncio
import pprint
import gpt_tweet, gpt_medium

TWITCH_USER_ID = "syntheticscode"
INTRODUCTION = f"""at SyntheticsCode we use chatGPT GPT-3 and copilot on coding projects and solve real-world problems.
Today we want to stream:
"""


async def set_stream_topic(stream_topic):
    client = await Twitch(app_id=key.TWITCH_CLIENT_ID, app_secret=key.TWITCH_CLIENT_SECRET)
    user = await first(client.get_users(logins=TWITCH_USER_ID))
    target_scope = [AuthScope.BITS_READ,AuthScope.CHANNEL_MANAGE_BROADCAST]
    auth = UserAuthenticator(client, target_scope, force_verify=False)
    token, refresh_token = await auth.authenticate()
    await client.set_user_authentication(token, target_scope, refresh_token)
    response = await client.modify_channel_information(
        title=stream_topic, broadcaster_id=user.id
    )
    print("Successfully set stream topic to:", stream_topic)

# insert await
async def main():

    topic = "Writing some automated python prompt that can turn any gpt-3 answer into json quickly and easily"

    prompt = f" i will be streaming on twitch at https://www.twitch.tv/syntheticscode "+ TOPIC
    id = gpt_tweet.generate_select_and_send_one(prompt,5)
    await set_stream_topic("Code with ChatGPT - Turn any gpt-3 answer into json")

    medium_response = gpt_medium.generate_and_publish_article("gpt_json.py")

    medium_link = medium_response["url"]
    prompt = f"stream is over, check the medium article about {topic} at {medium_link}"
    response_id = gpt_tweet.generate_select_and_send_one(prompt,tweet_id = response_id)

    twitch_link = input("twitch_link: ")
    prompt = f"stream is over, check the recording of the stream about {topic} at {twitch_link}"
    response_id = gpt_tweet.generate_select_and_send_one(prompt,tweet_id = response_id)


if __name__ == "__main__":
    asyncio.run(main())
