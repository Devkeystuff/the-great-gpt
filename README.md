# The Great GPT

The ultimate aid to the most notorious task known to human ('The Great Expectations' readers diary)

## Clone

    git clone git@github.com:Devkeystuff/the-great-gpt.git

## Requirements

- [Python ^3.9.5](https://www.python.org/)

## How to run

1.  [Clone](#clone) the repo
2.  OPTIONAL: create virtual environment

    ```
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  Install dependencies

    ```
    pip install -r requirements.txt
    pip install git+https://github.com/mmabrouk/chatgpt-wrapper
    playwright install
    ```

4.  Authenticate ChatGPT

    ```
    chatgpt install
    ```

5.  Run script

    ```
    python main.py
    ```
