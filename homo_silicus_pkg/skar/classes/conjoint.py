from skar.classes.survey import Surveys
from skar.analysis.numbers import *
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import *
from skar.subject.subject import Subject
from itertools import product, combinations


default_order = ["subject", "scenario", "round"]


class Conjoint(Surveys):
    def __init__(self, *args, num_choices=2, len_choices=0, name_columns=None, **kwds):
        # Parameter validation
        kwds["one_word"] = True
        self._choice_options = kwds["choices"]
        assert isinstance(self._choice_options, list) and all(
            isinstance(i, list) for i in self._choice_options)
        if name_columns:
            assert isinstance(name_columns, list) and all(
                isinstance(i, list) for i in self._choice_options), "column names must be provided as a list of strings"
            assert len(name_columns) == len(
                self._choice_options), "number of column names must equal number of choices"
        self._choices_map = {}
        for i in range(len(self._choice_options)):
            self._choices_map[i] = self._choice_options[i]

        # Conjoint-specific parameters
        # num_choices is the number of choices given in the prompt
        self._num_choices = num_choices
        # len_choices is the number from all possible lists of choices that are combined
        if len_choices == 0:
            self._len_choices = len(self._choice_options)
        else:
            assert len_choices <= len(self._choice_options)
            self._len_choices = len_choices

        # Create Survey via superclass
        super().__init__(*args, **kwds)

        # Create and feed back choices dictionary
        self._choices = self.build_conjoints()

    def format_choices(self, *args):
        return ", ".join(*args)

    def build_conjoints(self):
        all_choice_list_keys = self._choices_map.keys()
        all_choice_list_combinations = list(
            combinations(all_choice_list_keys, self._len_choices))
        all_choice_combinations = []
        for i in all_choice_list_combinations:
            curr_choice_combinations = list(
                product(*[list(range(len(self._choices_map[j]))) for j in i]))
            for c_i in curr_choice_combinations:
                all_choice_combinations.append(
                    tuple([(i[c_j], c_i[c_j]) for c_j in range(len(c_i))]))

        all_choice_combinations_mapped = {}
        for k in all_choice_combinations:
            all_choice_combinations_mapped[k] = [
                self._choices_map[c_k[0]][c_k[1]] for c_k in k]

        final_choices = {}
        final_choices_combinations = list(combinations(
            all_choice_combinations_mapped.keys(), self._num_choices))
        for l in final_choices_combinations:
            final_choices[tuple(l)] = [self.format_choices(
                all_choice_combinations_mapped[c_l]) for c_l in l]

        return final_choices

    def run_all(self):
        all_experiments = list(product(
            self._models, self._endowments, self._scenarios, self._tasks, self._choices, self._temperatures))
        all_results = {}

        # Run experiment for every combination of given parameters
        for model, endowment, scenario, task, choices_key, temperature in all_experiments:
            print(self._choices[choices_key])
            all_results[choices_key] = self.run_single_survey(
                model, endowment, scenario, task, self._choices[choices_key], temperature)
            print(all_results[choices_key]["choice"])
            print("-----------------------")

        return all_results
