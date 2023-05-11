import random

class Round:
    """
    The Round class holds an isolated set of tasks and choices and generates a corresponding
    prompt to individually run on a GPT model.

    Args:
        task (str): Main task or question
        choices (list of str): Choices available for the subject to choose
        transition (str): Optional parameter to add more information, after task
        instruction (str): Optional parameter to add instructions, after task and transition
    """

    def __init__(self, task, choices, transition=None, instruction="Your choices are the following:", randomize_choice_ordering=False):
        self._task = task
        self._choices = choices
        self._transition = transition
        self._instruction = instruction
        self._choices_order = {}
        if randomize_choice_ordering:
            new_choices_order = [i for i in range(len(choices))]
            random.shuffle(new_choices_order)
            new_choices = []
            for i, c in enumerate(new_choices_order):
                new_choices.append(choices[c])
                self._choices_order[c+1] = i
            self._choices = new_choices

    def generate_round_prompt(self):
        '''
        Generate prompt outlining tasks and choices available for the subject, with ennumerated choices.
        Contains bulk of survey or experiment information and instructions.
        Instructs GPT model to return answer as a single word/number for the chosen choice.
        '''
        round_prompt = self._task + "\n"
        if self._transition:
            round_prompt += self._transition + "\n"
        round_prompt += "\n"
        if self._instruction:
            round_prompt += self._instruction + "\n"
        for i, c in enumerate(self._choices):
            round_prompt += str(i+1) + ") " + c + "\n"

        round_prompt += "\n"
        round_prompt += f"""What is your choice, with one word: {list(range(1, 1+ len(self._choices)))}:"""
        return round_prompt
    
    def check_result(self, result):
        if len(self._choices_order) > 0:
            try:
                return self._choices_order[int(result)]
            except:
                return "Result not found"
        return result
