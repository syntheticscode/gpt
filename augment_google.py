import requests
from bs4 import BeautifulSoup
from gpt import gpt_api
from syntheticscode.google import key


def get_google_search_results(query, num_results=1):
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "cx": key.SYNTHETICS_CODE_CX_KEY,
        "q": query,
        "key": key.SYNTHETICS_CODE_API_KEY,
        "num": num_results,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [item["link"] for item in response.json()["items"]]


def gather_paragraphs_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    if not paragraphs:
        return ""
    return "\n".join([p.get_text() for p in paragraphs])


def gather_paragraphs_from_urls(urls):
    return [gather_paragraphs_from_url(url) for url in urls]


def ask_gpt_augmented(question, paragraph_list):
    sources = "\n".join(paragraph_list)
    prompt_augmented = (
        sources
        + "Based on your knowledge and this text (that might be irrelevant), answer only the following question:\n{}".format(
            question
        )
    )
    return gpt_api.respond(prompt_augmented)


def ask_gpt_how_to_google(question):
    prompt = f"How would you google the following question: {question}"
    return gpt_api.respond(prompt)


def ask_routine(question):
    print("question:", question, "\n")
    gpt_question = ask_gpt_how_to_google(question)
    print("gpt_question:", gpt_question, "\n")
    url = get_google_search_results(gpt_question)
    print("url found on google:", url, "\n")
    sources = gather_paragraphs_from_urls(url)
    response_augmented = ask_gpt_augmented(question, sources)
    print("augmented GPT response:\n", response_augmented, "\n")

    response_normal = gpt_api.respond(question)
    print("normal GPT response:\n", response_normal, "\n")


if __name__ == "__main__":
    question = "does Napoleon has some living heirs?"
    ask_routine(question)


"""     
example output:
question: does Napoleon has some living heirs?

augmented GPT response:
Yes, Napoleon has some living heirs. These include his great-great-grandson, Jean-Christophe, Prince Napoléon, and his great-great-great-grandson, Prince Louis Napoléon. Additionally, there are numerous descendants of Napoleon's illegitimate son, Count Alexandre Colonna-Walewski, and of his sister, Caroline Bonaparte.     #

normal GPT response:
Yes, Napoleon has living heirs. The current head of the House of Bonaparte is Prince Charles-Napoleon Bonaparte, a great-great-great-great-nephew of Napoleon I.
"""
