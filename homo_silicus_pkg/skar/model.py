import json
import os
import re
import sqlite3
import time
from threading import Thread

import dotenv
import openai
from dotenv import load_dotenv


class Model:
    def __init__(self, max_failures=4, timeout_seconds=30, models=["text-davinci-003"]):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self._max_failures = max_failures
        self._timeout_seconds = timeout_seconds
        self._models = models if type(models) == list else [models]

    def run_prompt(self, prompt):
        failure_count = 0
        results = []
        for model in self._models:
            while True and failure_count < self._max_failures:
                try:
                    choice_raw = openai.Completion.create(
                        model=model,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0
                    )
                    choice_text = choice_raw['choices'][0]['text'].strip()
                    results.append(dict({"choice_raw": choice_raw,
                                         "choice_text": choice_text,
                                         "choice": choice_text,
                                         "model": model,
                                         "prompt": prompt}))
                    break
                except openai.error.ServiceUnavailableError as e:
                    print(f"Experiment error: {e}")
                    failure_count += 1
                    time.sleep(self._timeout_seconds)
        return results


if __name__ == "__main__":
    print("Hello World")
