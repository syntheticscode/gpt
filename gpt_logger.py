import json, datetime, glob

ME = "syntheticscode: "
GPT = "GPT-3: "

JSON_structure = {
    "prompt": "a prompt",
    "answer": "a answer",
    "completion": "a completion",
}

# add a new json file every time this fucntion is called
# with the file name that include the current date and time
# in the folder called logs
def add_log(prompt, answer, completion):
    file_name = "log_" + str(datetime.datetime.now()).replace(" ", "_") + ".json"
    with open("logs/" + file_name, "w") as f:
        # make sure the json file is formatted
        json.dump(
            {
                "prompt": prompt,
                "answer": answer,
                "completion": completion,
                "file_name": file_name,
            },
            f,
            indent=4,
        )


# load all the json files in the folder called logs
def load_logs():
    return [json.load(open(filename, "r")) for filename in glob.glob("logs/*.json")]


def print_chat(prompt, answer):
    print("ME: ", prompt)
    print(" -" * 40)
    print("GPT-3: ", answer)
    print("#" * 80)


if __name__ == "__main__":
    for item in load_logs():
        print_chat(item["prompt"], item["answer"])
