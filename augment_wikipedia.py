import gpt.gpt_api as gpt_api
import pprint
from bs4 import BeautifulSoup
import requests
import json


def find_page_srsearch(search_string):
    base_url = "https://en.wikipedia.org/w/api.php"
    search_keys = get_gpt_tags(search_string)
    print(search_keys)
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": "+".join(search_keys),
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        search_results = response.json()
        if not search_results["query"]["search"]:
            raise RuntimeError(
                "No results found in wikipedia for '{}'".format(search_string)
            )
        results = search_results["query"]["search"]
        first_page = results[0]
        page_id = first_page["pageid"]
        page_title = first_page["title"]
        page_url = f"https://en.wikipedia.org/wiki/{page_title}"
        return page_url
    else:
        print("Error accessing API:", response.status_code)


def get_page_text(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error accessing API:", response.status_code)


def filter_page_text(page_text):
    soup = BeautifulSoup(page_text, "html.parser")
    paragraphs = soup.find("div", {"id": "mw-content-text"}).find_all("p")[:5]
    return "\n".join([p.text for p in paragraphs])


def respond_augmented(prompt):
    page_url = find_page_srsearch(prompt)
    page_text = get_page_text(page_url)
    filtered_text = filter_page_text(page_text)
    prompt_augmented = (
        filtered_text
        + "Based on your knowledge and this text aswer the following question:\n{}".format(
            prompt
        )
    )
    return gpt_api.respond(prompt_augmented)


def get_gpt_tags(prompt):
    question = """I want to search in wikipedia api for "{}" which key words should i use? respond only with a JSON in the format ["key1","key2",]""".format(
        prompt
    )
    response = gpt_api.respond(question)
    list = json.loads(response)
    return list


if __name__ == "__main__":
    question = "what is the longest river in sicily?"
    print("standard:", gpt_api.respond(question))
    print("augmented:", respond_augmented(question))
