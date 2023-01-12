import os

from chatgpt_wrapper import ChatGPT

PROMPTS = [
    "Summarize {}",
    "Describe the location where the action takes place in {}",
    "List the main characters involved in {}",
    "What questions do you have for the author after reading {}?",
    "What are your predictions on what could happen next after reading {}?",
    "What are some notable phrases or words used by the author in {}?",
    "What are your favorite quotes the author used in {}?"
]

def ask_questions(chapter: int):
    for prompt in PROMPTS:
        prompt = prompt.format("Chapter {}".format(chapter))
        if os.path.exists(f"{chapter}.txt"):
            with open(f"{chapter}.txt", "r") as file:
                prompt_exists = False
                for line in file:
                    if prompt in line:
                        prompt_exists = True
                if prompt_exists:
                    continue
        print(prompt + "\n")
        response = bot.ask(prompt)
        print(response)
        if response:
            save_answers(chapter, prompt, response)
        else:
            print(f"Failed to find an answer to: {prompt}")

def save_answers(chapter: str, question: str, answer: str, mode = "w"):
    if os.path.exists(f"{chapter}.txt"):
        mode = "a"
    with open(f"{chapter}.txt", mode) as file:
        file.write(question + "\n")
        file.write(answer + "\n\n")


if __name__ == "__main__":
    bot = ChatGPT()
    chapter_interval = input("How many chapters do you want to scrape?(e.g. 1-50): ")
    start, end = [int(chapter) for chapter in chapter_interval.split("-")]

    print("Initiating conversation...")
    response = bot.ask("I will ask you questions regarding the book 'The Great Expectations' (1998) by Charles Dickens")
    print(response)
    if not os.path.exists("chapters"):
        os.makedirs("chapters")
    os.chdir("chapters")

    for chapter in range(start, end + 1):
        ask_questions(chapter)
