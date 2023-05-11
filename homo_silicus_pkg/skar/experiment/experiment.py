from skar.experiment.round import Round
from skar.subject.endowments import Endowments
from skar.subject.subject import Subject


class Experiment:
    """
    The Experiment class holds all rounds, subjects, and endowments, and combines these
    iteratively to build all of the possible experiment prompts.

    Args:
        introduction (str): Introductory information
        rounds (list of Round): Rounds to iterate on
        subjects (list of Subject): Premade subjects for experiment, where each subject will
            participate in every round
        num_subjects (str): Number of subjects, should be same as length of subjects list
        endowments (list of endowments): Available endowments for the entire experiment
    """

    def __init__(self, introduction="", rounds=[], subjects=[], num_subjects=0, endowments=[]):
        self._introduction = introduction
        self._rounds = rounds
        self._subjects = subjects
        self._num_subjects = num_subjects
        assert self._num_subjects == len(self._subjects)
        self._endowments = endowments

    # Methods to manually add additional subjects and rounds after initialization

    def add_subject(self):
        self._subjects.append(Subject(self._num_subjects))
        self._num_subjects += 1

    def add_subject(self, subject):
        self._subjects.append(subject)

    def add_subjects(self, endowments=Endowments()):
        available_endowments = endowments.get_all_endowments()
        for e in available_endowments:
            self.add_subject(Subject(self._num_subjects, endowment=e))
            self._num_subjects += 1

    def add_round(self, round):
        self._rounds.append(round)

    def make_round(self, task, choices, transition=None, instruction=None, randomize_choice_ordering=False):
        self._rounds.append(Round(task, choices, transition,
                            instruction, randomize_choice_ordering))

    def generate_experiment_prompt(self):
        '''
        Generate all the possible experiment prompts, combining each of the subjects with
        each of the rounds.
        '''
        all_experiment_prompts = []

        experiment_prompt = self._introduction + "\n"
        for s in self._subjects:
            experiment_prompt_s = experiment_prompt + s.generate_endowment_prompt() + "\n"
            for r in self._rounds:
                experiment_prompt_r = experiment_prompt_s + r.generate_round_prompt() + "\n"
                all_experiment_prompts.append(experiment_prompt_r.strip())

        return all_experiment_prompts

    def generate_experiment_prompt_useround(self):
        '''
        Generate all the possible experiment prompts, combining each of the subjects with
        each of the rounds.
        '''
        all_experiment_prompts = []

        experiment_prompt = self._introduction + "\n"
        for s in self._subjects:
            experiment_prompt_s = experiment_prompt + s.generate_endowment_prompt() + "\n"
            for r in self._rounds:
                experiment_prompt_r = experiment_prompt_s + r.generate_round_prompt() + "\n"
                all_experiment_prompts.append((experiment_prompt_r.strip(), r))

        return all_experiment_prompts
