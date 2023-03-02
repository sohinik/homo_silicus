class Round:
    def __init__(self, task, choices, instruction="Your choices are the following:", transition=""):
        self._task = task
        self._instruction = instruction
        self._choices = choices
        self._transition = transition

    def generate_round_prompt(self):
        round_prompt = self._task + "\n"
        if self._instruction:
            round_prompt += self._instruction + "\n"
        for i, c in enumerate(self._choices):
            round_prompt += str(i) + ") " + c + "\n"

        round_prompt += f"""What is your choice, with one word: {list(range(len(self._choices)))}:"""
        return round_prompt
