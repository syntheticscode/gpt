import json
import gpt_api


# create a class that can be initialized with a dict
class Person:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


# really nice that it is a felxible dict and can be used for any json
bio_json_format = {
    "birth_date": "1999-01-01",
    "death_date": "2021-01-01",
    "cause_of_death": "",
    "name": "",
    "best_known_for": "",
    "greatness_rate_from_1_to_10": 0,
    "nationality": "",
}

# returns a dict given a topic and a json format to follow
# tries_left is used to try again if the response is not a valid json
def respond_json(topic: str, json_format: dict, tries_left: int = 2) -> dict:
    prompt = (
        f"Here is a topic for you to analyze:\n\n"
        f'"{topic}"'
        f"\n\nNow, I want you to respond to me by filling a JSON that follows this format. "
        f"Reply only with a JSON:\n\n```\n{json.dumps(json_format, indent=4)}\n```"
    )
    try:
        response = json.loads(gpt_api.respond(prompt))
    except json.decoder.JSONDecodeError:
        if tries_left == 0:
            print("Error: the response is not a valid JSON again. giving up.")
            return None
        print(
            f"Error: the response is not a valid JSON. trying again. tries left = {tries_left}..."
        )
        return respond_json(topic, json_format, tries_left - 1)
    return response


if __name__ == "__main__":
    # test
    alexander = Person(**respond_json("Alexander the great", bio_json_format))
    print(alexander)
