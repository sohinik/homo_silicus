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

from threading import Thread

openai.api_key = os.getenv('OPENAI_API_KEY')

total = 100

def create_prompt(total):
    total_b_1 = total/3
    total_a_1 = 2*total/3
    total_b_2 = 2*total/5
    total_a_2 = 3*total/5
    prompt = """You are deciding on allocation for yourself and another person, Person A.

    Option Left:  You get ${total_b_1}, Person A gets ${total_a_1}
    Option Right: You get ${total_b_2}, Person A gets ${total_a_2}

    What do you choose, with one word [Left, Right]? Explain why."""
    return prompt
    
MAX_FAILURES = 4

def get_decision(total = 100, model = "text-davinci-003"):
    prompt = create_prompt(total)
    failure_count = 0
    while True and failure_count < MAX_FAILURES:
        try:
            choice_raw = openai.Completion.create(
                model= model,
                prompt = prompt,
                max_tokens=150,
                temperature=0
            )
            choice_text = choice_raw['choices'][0]['text'].strip()
            break
        except openai.error.ServiceUnavailableError as e:
            print(f"Experiment error: {e}")
            failure_count += 1 
            time.sleep(30)          

    return dict({"choice_raw": choice_raw,
                 "choice_text": choice_text,
                 "choice": choice_text,
                 "model":model,
                 "prompt":prompt})

class GetKKTChoiceThread(Thread):

    def __init__(self, total, model):
        super().__init__()
        self.total = total
        self.model = model

    def run(self):
        self.decision = get_decision(total = self.total, model = self.model)

models = ["text-davinci-003"]

threads = []
for model in models:
    thread = GetKKTChoiceThread(total = total, model = model)
    thread.start()
    threads.append(thread)
    
observations = []
for thread in threads:
    thread.join()
    observations.append(thread.decision)

print(observations)
