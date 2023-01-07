import gpt_api
import key
from medium import Client
from pprint import pprint


def read_python_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


# write an article with gpt-3
def write_article(code: str):
    prompt = f"""Write a Medium article about the following python code with snippets. Use Markdown and add a catchy headline in the first line, remeber to annotate the makrdown code with the language:\n```python\n{code}\n```\n"""
    answer = gpt_api.respond(prompt, max_tokens=2800)
    # get the first line of answer and use it as title, remove any "#"
    title = answer.splitlines()[0].replace("#", "").strip()
    return title, answer


# publish the article to medium with medium api
def publish_article(title: str, content: str):
    client = Client(access_token=key.MEDIUM_TOKEN)
    tags = ["python", "coding", "gpt-3"]
    post = client.create_post(
        title=title,
        content=content,
        tags=tags,
        user_id=client.get_current_user()["id"],
        content_format="markdown",
        publish_status="draft",
    )
    pprint(post)
    return post

# generate and publish an article given file path
def generate_and_publish_article(path: str):
    python_file = read_python_file(path)
    title, article = write_article(python_file)
    return publish_article(title, article)

if __name__ == "__main__":
    generate_and_publish_article("gpt_json.py")
