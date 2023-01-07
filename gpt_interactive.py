import gpt_api

if __name__ == "__main__":
    while True:
        print(
            "GPT-3: ",
            gpt_api.code(input("code: "))
            if input("(t)alk? or (c)ode:").upper == "C"
            else gpt_api.talk(input("talk: ")),
        )
