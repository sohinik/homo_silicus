from skar.experiment.experiment import Experiment
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import Endowments

"""
GENERAL STRUCTURE
    Experiment - individual prompt
        Introduction
        Subject Endowment Prompt
            Preset parameters (age, gender, etc)
            Additional parameters
        Round
            Task
            Transition
            Instructions
            Choices
            "What choice... [pick one word/number]"
"""

# Generate all political alignments for subject endowments
political = [
    "socialist",
    "leftist",
    "liberal",
    "moderate",
    "liberterian", 
    "conservative",
]

# Generate all the tasks
all_tasks = []
scenarios_storeaction = ["changes the price to", "raises the price to"]
scenarios_newprice = [16, 20, 40, 100]
for action in scenarios_storeaction:
    for price in scenarios_newprice:
        all_tasks.append(f"""A hardware store has been selling snow shovels for $15. The morning after a large snowstorm, the store {action} ${price}.""")

all_choices = ["Completely Fair", "Acceptable", "Unfair", "Very Unfair"]

# Used for storing results
finals = [[]]


def run_experiment_kkt():
    model = Model()
    experiment = Experiment()

    for t in all_tasks:
        experiment.add_round(task=t, choices=all_choices)

    endowments = Endowments(political=political)

    experiment.add_subjects(endowments)

    prompts = experiment.generate_experiment_prompt()

    # Run prompts and print corresponding results
    for p in prompts:
        print(p)
        print([i["choice_text"] for i in model.run_prompt(p)])
        print("-----------------------------------------------")
        if len(finals[-1]) >= len(scenarios_newprice):
            finals.append([])
        finals[-1].extend([i["choice_text"] for i in model.run_prompt(p)])

    print(finals)
    
    