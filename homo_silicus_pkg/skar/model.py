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
    """
    The Model class initiates preliminary parameters for creating a GPT model
    and setting necessary error-handling variables.

    Args:
        max_failures (int): Number of times to try sending a prompt
        timeout_seconds (int): Amount of time to wait before re-sending prompt
        models (list): GPT models to call
    """

    def __init__(self, max_failures=4, timeout_seconds=30, models=["text-davinci-003"]):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self._max_failures = max_failures
        self._timeout_seconds = timeout_seconds
        self._models = models if type(models) == list else [models]

    def run_prompt(self, prompt, num_choices=None, temperature=1):
        '''
        Run the given prompt using the model settings set by the class

        Args:
            prompt (string): Prompt for GPT model
            num_choices (int): Number of most likely tokens to return logprobs for

        Raises:
            ServiceUnavailableError: OpenAI Error, error handling to retry a couple times
            without raising error

        Returns:
            results (list): GPT results for given prompt
        '''
        if num_choices:
            num_choices = max(5, num_choices)

        failure_count = 0
        results = []
        for model in self._models:
            while failure_count < self._max_failures:
                try:
                    # Create model and run prompt
                    # https://platform.openai.com/docs/api-reference/completions/create
                    choice_raw = openai.Completion.create(
                        model=model,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=temperature,
                        logprobs=num_choices,
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
