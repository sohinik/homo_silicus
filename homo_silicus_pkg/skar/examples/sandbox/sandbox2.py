from threading import Thread
import os

import dotenv
import json
import re
import openai
import time
import sqlite3
import json

from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')

MAX_FAILURES = 4
model = "text-davinci-003"

failure_count = 0
prompt1 = "To be or not to be, that is the:"

while True and failure_count < MAX_FAILURES:
    try:
        choice_raw = openai.Completion.create(
            model=model,
            prompt=prompt1,
            max_tokens=150,
            temperature=0
            )
        choice_text = choice_raw['choices'][0]['text'].strip()
        break
    except openai.error.ServiceUnavailableError as e:
        print(f"Experiment error: {e}")
        failure_count += 1
        time.sleep(30)

print(dict({"choice_raw": choice_raw,
    "choice_text": choice_text,
    "choice": choice_text,
    "model":model,
    "prompt":prompt1}))


failure_count = 0
prompt2 = "What was the previous input?"

while True and failure_count < MAX_FAILURES:
    try:
        choice_raw = openai.Completion.create(
            model=model,
            prompt=prompt2,
            max_tokens=150,
            temperature=0
            )
        choice_text = choice_raw['choices'][0]['text'].strip()
        break
    except openai.error.ServiceUnavailableError as e:
        print(f"Experiment error: {e}")
        failure_count += 1
        time.sleep(30)

print(dict({"choice_raw": choice_raw,
    "choice_text": choice_text,
    "choice": choice_text,
    "model":model,
    "prompt":prompt2}))


failure_count = 0
prompt3 = ["How are you?", "What was the previous input?"]

while True and failure_count < MAX_FAILURES:
    try:
        choice_raw = openai.Completion.create(
            model=model,
            prompt=prompt3,
            max_tokens=150,
            temperature=0
            )
        choice_text = choice_raw['choices'][0]['text'].strip()
        break
    except openai.error.ServiceUnavailableError as e:
        print(f"Experiment error: {e}")
        failure_count += 1
        time.sleep(30)

print(dict({"choice_raw": choice_raw,
    "choice_text": choice_text,
    "choice": choice_text,
    "model":model,
    "prompt":prompt3}))