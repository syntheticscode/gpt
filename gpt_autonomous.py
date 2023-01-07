import gpt_api
import json
from pprint import pprint

text = f"""

"""

"""
- unorganized way
    - just provide a framework for gpt to call itself
- organized way
    - create roles ourselves 
        - ideation
        - design
        - implementation
        - testing
        - deployment
        - maintenance
        - documentation
"""

INSTRUCTIONS = "instructions"
CODE = "code"

json_instruction = {
    INSTRUCTIONS: ["first instruction", "second Instruction", "third instruction"]
}
json_code = {
    CODE: "here write some python code to do the task",
}


def get_prompt(task: str, parents: list):
    if not parents:
        parents_str = ""
    else:
        parents_str = (
            "Because i am trying to: "
            + " , Because i am trying to: ".join(parents)
            + "\n"
        )

    return f"""I need to to {task}:
    {parents_str}If the task is simple enoguh for you to code it, reply with {json.dumps(json_code)}. Else, reply with {json.dumps(json_instruction)}.
    """


def call_gpt(task, parents, iter=0):
    if not iter:
        return
    print("call_gpt():", iter, task, parents)
    prompt = get_prompt(task, parents)
    response_string = gpt_api.respond(prompt)
    parents.append(task)

    # try catch in case json is not valid
    try:
        response = json.loads(response_string)
    except:
        print("invalid json: ")
        pprint(response_string)
        return

    if INSTRUCTIONS in response:
        print("////", INSTRUCTIONS, response[INSTRUCTIONS])

        for instruction in response[INSTRUCTIONS]:
            call_gpt(instruction, parents, iter - 1)
        return
    elif CODE in response:

        print("////", CODE, response[CODE])
        return
    else:
        print("invalid response: ")
        print(response)


# main function
def main():
    task = "A personal finance tracker app with python"
    call_gpt(task, [], iter=2)


if __name__ == "__main__":
    main()
