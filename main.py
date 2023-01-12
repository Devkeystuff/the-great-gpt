import multiprocessing
import os

from chatgpt_wrapper import ChatGPT

PROMPTS = [
    "How many pages are there in {}?",
    "Summarize {}",
    "List all the characters involved in {}",
    "What questions do you have for the author after reading {}?",
    "What are your predictions on what could happen next after reading {}?",
    "What are the most interesting expresions the author used in the {}?",
    "Give 5 quotes from {}"
]

def enable_multicore(autoenable=False, maxcores=None, buffercores=1):
    native_cpu_count = multiprocessing.cpu_count() - buffercores
    if autoenable:
        if maxcores:
            if(maxcores <= native_cpu_count):
                return maxcores
            else:
                print("Too many cores requested, single core operation fallback")
                return 1
        return multiprocessing.cpu_count() - 1
    multicore_query = input("Enable multiprocessing (Y or N): ")
    if multicore_query not in ["Y","y","Yes","YES","YEs",'yes']:
        return 1
    core_count_query = int(input("Max core count (0 for allcores): "))
    if(core_count_query == 0):
        return native_cpu_count
    if(core_count_query <= native_cpu_count):
        return core_count_query
    else:
        print("Too many cores requested, single core operation fallback")
        return 1

class Prompts:
    def __init__(self, chapters: int) -> None:
        self.chapters = chapters
        self._current_chapter = None

    def ask_questions(self, chapter: int):
        self._current_chapter = chapter
        for prompt in PROMPTS:
            prompt = prompt.format("Chapter {}".format(chapter))
            print(prompt + "\n")
            response = bot.ask(prompt)
            print(response)
            if response:
                self.__save_answers(prompt, response)
            else:
                print(f"Failed to find an answer to: {prompt}")

    def __save_answers(self, question: str, answer: str, mode = "w"):
        if os.path.exists(f"{self._current_chapter}.txt"):
            mode = "a"
        with open(f"{self._current_chapter}.txt", mode) as file:
            file.write(question + "\n")
            file.write(answer + "\n\n")

def multicore_get_chapters(chapters: int, cpu_count: int):
    chapters_per_cpu = chapters // cpu_count
    extra_chapters = chapters % cpu_count

    cpu_count_list = []
    for cpu in range(cpu_count):
        chapters = chapters_per_cpu
        if cpu < extra_chapters:
            chapters += 1
        cpu_count_list.append(chapters)

    print(cpu_count_list)
    processes = []
    segment_index = 0


if __name__ == "__main__":
    bot = ChatGPT()
    multicore_support = enable_multicore(autoenable=False, maxcores=None, buffercores=1)
    chapters = int(input("How many chapters do you want to scrape?(0-50): "))

    print("Initiating conversation...")
    response = bot.ask("I will ask you questions regarding the book 'The Great Expectations' (1998) by Charles Dickens")
    print(response)
    prompts = Prompts(chapters)
    if not os.path.exists("chapters"):
        os.makedirs("chapters")
    os.chdir("chapters")
    # for chapter in range(1, chapters + 1):
    #     prompts.ask_questions(chapter)

    if multicore_support > 1:
        multicore_get_chapters(chapters, multicore_support)