import os

from chatgpt_wrapper import ChatGPT

from bs4 import BeautifulSoup
import re

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
    #chapter that we will make chatgpt read
    chapter_pieces = []

    #fetch raw chapter text
    with open('../great_expectation.htm', 'r') as f:

        #read page
        contents = f.read()

        #parse page
        soup = BeautifulSoup(contents, 'html.parser')

        #find chapter
        chap = soup.find("a", {"name": "chap{0}".format(str('2').zfill(2))})
        chap_text = chap.parent.parent.get_text()

        for part in split_by_number_of_words(chap_text, 1998):
            chapter_pieces.append(part)

    for chapter_piece in chapter_pieces:
        rsp = bot.ask("""here's a part of chapter {0}, : "{1}" """.format(chapter, chapter_pieces))
        print(rsp)
    
    for prompt in PROMPTS:
        prompt = prompt.format("chapter {}".format(chapter))
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
    
    rsp = bot.ask("That's all for this chapter, can I give you another one?")
    print(rsp)

def save_answers(chapter: str, question: str, answer: str, mode = "w"):
    if os.path.exists(f"{chapter}.txt"):
        mode = "a"
    with open(f"{chapter}.txt", mode) as file:
        file.write(question + "\n")
        file.write(answer + "\n\n")

def split_by_number_of_words(input, number_of_words):
    regexp = re.compile(r'((?:\w+\W+){0,%d}\w+)' % (number_of_words - 1))
    return regexp.findall(input)

if __name__ == "__main__":
    bot = ChatGPT()
    chapter_interval = input("Which chapters do you want to scrape?(e.g. 1-50): ")
    start, end = [int(chapter) for chapter in chapter_interval.split("-")]

    print("Initiating conversation...")
    response = bot.ask("Can I give you a chapter from a book and then ask some questions about it?")
    print(response)
    if not os.path.exists("chapters"):
        os.makedirs("chapters")
    os.chdir("chapters")

    for chapter in range(start, end + 1):
        ask_questions(chapter)
