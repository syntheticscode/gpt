import feedparser
import gpt_api
from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup


"""
- get an rss link. DONE
- learn how to parse it and find links. DONE
- learn how to parse the title, body, and so on. DONE
- generate title, summary and some tags. DONE
- present it back to the user. DONE
"""

json_format = {
    "title": "Title",
    # "intro": "This is a single line introduction to the article",
    "summary": "This is a few line summary",
    # "long_summary": "This is a longer summary",
    # "readability_0to10": 0,
    "minutes_to_read": 0,
    # "is_tech_article": True,
    "explain_like_im_5": "This is a short explanation of the article in simple words",
    "tags": ["tag1", "tag2", "tag3"],
}

# get the rss page and parse it
def get_rss(rss_link):
    rss = feedparser.parse(rss_link)
    return rss


# given a link of a blog web page get the full body text in one string
def get_text_from_url(link: str) -> str:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    # join all the paragraphs into one string
    return "\n".join([paragraph.get_text() for paragraph in paragraphs])


def process_article(article: str) -> dict:
    message = f"{article} After reading this article, respond with only a json in this format: {json.dumps(json_format)}"
    try:
        processed = json.loads(gpt_api.respond(message))
    except json.decoder.JSONDecodeError as e:
        return None
    return processed


# Given an rss entry, get the text from the link and process it
def process_rss_entry(entry: feedparser.FeedParserDict) -> None:
    text = get_text_from_url(entry.link).strip()[:10000]
    if len(text) < 100:
        print(f"Could not get text from {entry.title},{entry.link}.")
        return
    processed = process_article(text)
    if processed is None:
        print(f"Could not process the anseer for {entry.title},{entry.link}.")
        return
    # print_processed(entry, processed)
    pprint(processed)
    return


def print_processed(entry, processed: dict) -> None:
    print(processed["title"], "[", processed["minutes_to_read"], " min ]")
    print("Tags:", ", ".join(processed["tags"]))
    print(entry.link)
    print()
    print(processed["summary"])


def main():
    rss_link = "https://news.ycombinator.com/rss"
    rss = get_rss(rss_link)
    print(rss.feed.title, "Rss Feed - AUGMENTED WITH GPT-3")
    for item in rss.entries[:10]:
        print(" -" * 40)
        process_rss_entry(item)


if __name__ == "__main__":
    main()
