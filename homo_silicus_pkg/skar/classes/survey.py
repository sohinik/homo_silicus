import json
import sqlite3
import time
from skar.analysis.numbers import *
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import *
from skar.subject.subject import Subject
from itertools import product


default_order = ["subject", "scenario", "round"]
modules = ["model", "endowment", "scenario", "task", "choices", "temperature"]
class_parameters = ["models", "endowments", "scenarios", "tasks", "choices", "order",
                    "num_runs", "randomize_choice_ordering", "one_word", "temperatures",
                    "logprobs"]


class Surveys:
    """
    The Surveys class represents a type of economic experiment, the general survey.
    Taking in various inputs, it iterates through all possible combinations and runs the corresponding
    prompts.

    Args:
        models (Model or list of Model): Mdels to use to run prompts
        endowments (Endowment or Endowments): Endowments to use in building prompts
        scenarios (list of str, optional): Preliminary scenario to introduce context for choices
        tasks (str or list of str, optional): Specific task or question
        choices (list of str, optional): Sets of possible choices
        order (list of str, optional): Order of the various modules
        num_runs (int, optional): Number of times to run each possible experiment (to be implemented)
        randomize_choice_ordering (boolean, optional): Whether to randomize order of choices as presented
        one_word (boolean, optional): Whether to instruct model to return answer as one word
        temperatures (float or list of float, optional): Temperatures to run experiments at
        logprobs (bool or int, optional): Whether to return the probabilities
    """

    def __init__(self, models, endowments, scenarios=[""], tasks="", choices=[[""]],
                 order=default_order, num_runs=1, randomize_choice_ordering=False, one_word=True,
                 temperatures=[1], logprobs=None):
        # Parameter validation
        assert ((isinstance(models, list) and all(
            (isinstance(i, Model) for i in models))) or isinstance(models, Model)), "models parameter must be a Model object or list of Model objects"
        assert (isinstance(endowments, Endowments)
                or isinstance(endowments, Endowment)), "endowments parameter must be an Endowment object or Endowments object"
        assert isinstance(
            scenarios, list), "scenarios must be a list or strings"
        assert (isinstance(tasks, str) or isinstance(tasks, list)
                ), "tasks must be a string or list of strings"
        assert isinstance(choices, list), "choices must be a list"
        assert isinstance(order, list) and set(order) == set(
            default_order), f"order must be a an ordered list of the following options: {default_order}"
        assert isinstance(num_runs, int), "num_runs must be an integer"
        assert isinstance(randomize_choice_ordering,
                          bool), "randomize_choice_ordering must be a boolean"
        assert isinstance(one_word, bool), "one_word must be a boolean"
        assert (isinstance(temperatures, list)
                or (isinstance(temperatures, float) and temperatures >= 0 and temperatures <= 2)), "temperatures must be a float or list of floats between 0.0 and 2.0"
        assert (isinstance(logprobs, bool)
                or (isinstance(logprobs, int) and logprobs >= 0 and logprobs <= 5)), "logprobs must be a boolean or integer between 0 and 5"

        # Convert models, endowments, scenarios, and tasks into lists if not already
        self._models = models if isinstance(models, list) else [models]
        # self._endowments = endowments.get_all_endowments() if isinstance(
        #     endowments, Endowments) else [endowments] # Commented out to aid in JSONizing
        self._endowments = [endowments] if isinstance(
            endowments, Endowment) else endowments
        self._scenarios = scenarios
        self._tasks = tasks if isinstance(tasks, list) else [tasks]

        # General conversions depending on validation
        self._temperatures = temperatures if isinstance(
            temperatures, list) else [temperatures]
        self._logprobs = 5 if logprobs is True else logprobs

        # Set remaining parameters
        self._choices = choices if all(
            (isinstance(i, list) for i in choices)) else [choices]
        self._order = order
        self._num_runs = num_runs
        self._randomize_choice_ordering = randomize_choice_ordering
        self._one_word = one_word
        self._subject_id = 1

    def run_single_survey(self, model, endowment, scenario, task, choices, temperature=1):
        """
        Build and run one iteration of a prompt.

        Args:
            model (Model): Model to run prompt on
            endowment (Endowment): Endowment to build current subject from
            scenario (str): Preliminary scenario prompt
            task (str): Task for the subject
            choices (list of str): Set of possible choices
            temperature (int, optional): Temperature to run prompt at. Defaults to 1

        Returns:
            dict: Dictionary with all parameters, built prompt, and results
        """
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
        """
        Run all possible iterations of prompts from class parameters.

        Returns:
            list: list of all result dictionaries
        """
        # Build every combination of possible experiments
        endowments = self._endowments if isinstance(
            self._endowments, list) else self._endowments.get_all_endowments()
        all_experiments = list(product(
            self._models, endowments, self._scenarios, self._tasks, self._choices, self._temperatures))
        all_results = []

        # Run experiment for every combination of given parameters
        for model, endowment, scenario, task, choices, temperature in all_experiments:
            current_results = self.run_single_survey(
                model, endowment, scenario, task, choices, temperature)
            all_results.append(current_results)

        return all_results

    def run_all_write_data(self, database_string=f"../homo_silicus_pkg/skar/data/experiment_{time.time()}.db", flush=False, additional_tables=[]):
        """
        Run all possible iterations of prompts from class parameters and write to a database.

        Args:
            database_string (str, optional): Name of file to write data to. Defaults based on time
            flush (bool, optional): Whether to clear database if necessary. Defaults to False
            additional_tables (list, optional): Additional tables to create based on parameter. Defaults to []

        Returns:
            _type_: _description_
        """
        assert set(additional_tables).issubset(
            set(modules)), f"can only make additional tables for: {modules}"

        # Initialize tables
        conn = sqlite3.connect(database_string)
        cursor = conn.cursor()
        if flush:
            cursor.execute("DROP TABLE IF EXISTS responses")
            cursor.execute("DROP TABLE IF EXISTS experiments")
            for i in additional_tables:
                cursor.execute(f"DROP TABLE IF EXISTS {i}")
        cursor.execute("CREATE TABLE IF NOT EXISTS experiments (note TEXT)")
        cursor.execute("INSERT INTO experiments VALUES (?)",
                       (f"Experiment:{time.time()}",))
        experiment_id = cursor.lastrowid
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS responses (experiment_id INTEGER, choice TEXT, results TEXT, FOREIGN KEY(experiment_id) REFERENCES experiments(id))")
        for i in additional_tables:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {i} (experiment_id INTEGER, {i} TEXT, choice TEXT, results TEXT, FOREIGN KEY(experiment_id) REFERENCES experiments(id))")

        # Build every combination of possible experiments
        endowments = self._endowments if isinstance(
            self._endowments, list) else self._endowments.get_all_endowments()
        all_experiments = list(product(
            self._models, endowments, self._scenarios, self._tasks, self._choices, self._temperatures))
        all_results = []

        # Run experiment for every combination of given parameters
        for model, endowment, scenario, task, choices, temperature in all_experiments:
            current_results = self.run_single_survey(
                model, endowment, scenario, task, choices, temperature)
            all_results.append(current_results)
            cursor.execute("INSERT INTO responses VALUES (?,?,?)", (experiment_id, json.dumps(
                current_results["choice"]), json.dumps(current_results)))
            for i in additional_tables:
                cursor.execute(f"INSERT INTO {i} VALUES (?,?,?,?)", (experiment_id, str(
                    locals()[i]), json.dumps(current_results["choice"]), json.dumps(current_results)))
            conn.commit()

        return all_results

    def to_json(self, file_name):
        def serialize(obj):
            """
            Serializer to help handle non-JSON-serializable classes
            """
            if isinstance(obj, Endowments) or isinstance(obj, Endowment) or isinstance(obj, Model):
                serial = obj.to_dict()
                return serial

            return obj.__dict__

        with open(file_name, 'w') as f:
            print({"Surveys": self})
            f.write(json.dumps({"Surveys": self}, default=serialize))
            f.close()

    def from_json(file_name):
        json_file = open(file_name)
        json_obj = json.load(json_file)
        try:
            json_obj = json_obj["Surveys"]
        except:
            raise Exception("Attempting to build wrong class from JSON")
        json_file.close()
        json_obj_cleaned = {}
        models, endowments = None, None
        for key in json_obj:
            if key == "_models":
                models = Model.from_dict(json_obj[key]) if isinstance(json_obj[key], Model) else [Model.from_dict(i) for i in json_obj[key]]
            elif key == "_endowments":
                endowments = Endowments.from_dict(json_obj[key]) # Check if Endowment object?
            elif key[0] == "_":
                if key[1:] in class_parameters:
                    json_obj_cleaned[key[1:]] = json_obj[key]
            elif key in class_parameters:
                json_obj_cleaned[key] = json_obj[key]
        try:
            print(models)
            print(endowments)
            print(json_obj_cleaned)
            return Surveys(models, endowments, **json_obj_cleaned)
        except:
            raise Exception("JSON has the incorrect keys")
