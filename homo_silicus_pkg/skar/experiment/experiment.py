from skar.experiment.round import Round
from skar.subject.endowments import Endowments
from skar.subject.subject import Subject


class Experiment:
    def __init__(self, introduction="", rounds=[], subjects=[], num_subjects=0, endowments=[]):
        self._introduction = introduction
        self._rounds = rounds
        self._subjects = subjects
        self._num_subjects = num_subjects
        self._endowments = endowments

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

    def add_round(self, task, choices, instruction=None):
        self._rounds.append(Round(task, choices, instruction))

    def generate_experiment_prompt(self):
        all_experiment_prompts = []
        # print("self._subjects", self._subjects)
        # print("self._rounds", self._rounds)

        experiment_prompt = self._introduction + "\n"
        for s in self._subjects:
            experiment_prompt_s = experiment_prompt + s.generate_endoment_prompt() + "\n"
            for r in self._rounds:
                experiment_prompt_r = experiment_prompt_s + r.generate_round_prompt() + "\n"
                all_experiment_prompts.append(experiment_prompt_r.strip())

        return all_experiment_prompts
