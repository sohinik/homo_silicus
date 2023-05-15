from skar.analysis.numbers import *
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import *
from skar.subject.subject import Subject
from itertools import product


default_order = ["subject", "scenario", "round"]


class Surveys:
    def __init__(self, models, endowments, scenarios=[""], tasks="", choices=[[""]],
                 order=default_order, num_runs=1, analysis=False, randomize_choice_ordering=False, one_word=True,
                 temperatures=[1], get_logprobs=None):
        # Parameter validation
        assert (isinstance(models, list) or isinstance(models, Model))
        assert (isinstance(endowments, Endowments)
                or isinstance(endowments, Endowment))
        assert isinstance(scenarios, list)
        assert (isinstance(tasks, str) or isinstance(tasks, list))
        assert isinstance(choices, list)
        assert isinstance(order, list) and set(order) == set(default_order)
        assert isinstance(num_runs, int)
        assert isinstance(analysis, bool)
        assert isinstance(analysis, bool)
        assert isinstance(one_word, bool)
        assert (isinstance(temperatures, list)
                or (isinstance(temperatures, float) and temperatures >= 0 and temperatures <= 2))
        assert (isinstance(get_logprobs, bool)
                or (isinstance(get_logprobs, int) and get_logprobs >= 0 and get_logprobs <= 5))

        # Convert models, endowments, scenarios, and tasks into lists if not already
        self._models = models if isinstance(models, list) else [models]
        self._endowments = endowments.get_all_endowments() if isinstance(
            endowments, Endowments) else [endowments]
        self._scenarios = scenarios
        self._tasks = tasks if isinstance(tasks, list) else [tasks]

        # General conversions depending on validation
        self._temperatures = temperatures if isinstance(
            temperatures, list) else [temperatures]
        self._logprobs = 5 if get_logprobs is True else get_logprobs

        # Set remaining parameters
        self._choices = choices if all(
            (isinstance(i, list) for i in choices)) else [choices]
        self._order = order
        self._num_runs = num_runs
        self._analysis = analysis
        self._randomize_choice_ordering = randomize_choice_ordering
        self._one_word = one_word
        self._subject_id = 1

    def run_single_survey(self, model, endowment, scenario, task, choices, temperature=1):
        subject = Subject(self._subject_id, endowment=endowment)

        round = Round(task, choices,
                      randomize_choice_ordering=self._randomize_choice_ordering, one_word=self._one_word)

        prompt_components = {
            "subject": subject.generate_endowment_prompt(),
            "scenario": scenario,
            "round": round.generate_round_prompt(),
        }

        experiment_prompt = ""
        for component in self._order:
            experiment_prompt += prompt_components[component] + "\n"

        # Returns choice_raw, choice_text, model, prompt; can take first index since only 1 model
        results = model.run_prompt(
            experiment_prompt, temperature=temperature, num_choices=self._logprobs)[0]
        results["scenario"] = scenario
        results["endowment"] = endowment.get_endowment()
        results["task"] = task

        # Clean given results, to the extent possible based on chosen parameters
        try:
            result_choice_text = results["choice_text"]
            result = strip_complex(result_choice_text[0])
            if self._one_word:
                if not is_number(result):
                    result = text2int_simple(result)
                if self._randomize_choice_ordering:
                    result = round.check_result(result)
            else:
                results["choice_order"] = round.get_choices_order()
        except:
            print("Error cleaning results for Subject ID: ", self._subject_id)

        # Get log probabilities if selected in chosen parameters
        try:
            if self._logprobs:
                prob = 0
                for i in range(len(results["choice_raw"]["choices"][0]["logprobs"]["tokens"])):
                    if results["choice_raw"]["choices"][0]["logprobs"]["tokens"][i].strip() != "":
                        prob = results["choice_raw"]["choices"][0]["logprobs"]["token_logprobs"][i]
                results["log_prob"] = convert_logits(prob)
        except:
            print("Error extracting log probs for Subject ID: ", self._subject_id)

        results["choice"] = result

        self._subject_id += 1
        return results

    def run_all(self):
        all_experiments = list(product(
            self._models, self._endowments, self._scenarios, self._tasks, self._choices, self._temperatures))
        all_results = []

        # Run experiment for every combination of given parameters
        for model, endowment, scenario, task, choices, temperature in all_experiments:
            all_results.append(self.run_single_survey(
                model, endowment, scenario, task, choices, temperature))

        return all_results