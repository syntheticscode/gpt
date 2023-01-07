import gpt_logger as gpt_logger
import openai
import gpt.key as key
import enum

openai.api_key = key.GPT_KEY


class engine(enum.Enum):
    TEXT = "text-davinci-003"
    CODE = "code-davinci-002"


def respond(prompt, engine=engine.TEXT, max_tokens=1024, n=1, stop=None, temp=0.5):
    completions = openai.Completion.create(
        engine=engine.value,  # Set the engine to use
        prompt=prompt,  # Set the prompt
        max_tokens=max_tokens,  # Set the maximum number of tokens (words and punctuation) in the generated text
        n=n,  # Set the number of completions to generate
        stop=stop,  # Do not stop generating text until the maximum number of tokens is reached
        temperature=temp,  # Set the "temperature" parameter to control the randomness of the generated text
    )
    answer = completions.choices[0].text.strip()
    gpt_logger.add_log(prompt, answer, completions)
    return answer

if __name__ == "__main__":
    print(respond("Hello world!"))