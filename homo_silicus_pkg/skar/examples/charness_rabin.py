from skar.experiment.experiment import Experiment
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import Endowments

scenarios = dict({
    "Berk29": ((400, 400), (750, 400)),
    "Berk26": ((0, 800), (400, 400)),
    "Berk23": ((800, 200), (0, 0)),
    "Berk15": ((200, 700), (600, 600)),
    "Barc8": ((300, 600), (700, 500)),
    "Barc2": ((400, 400), (750, 375)),
})

parameters = [
    "",
    "You only care about fairness between players.",
    "You only care about the total pay-off of both players.",
    "You only care about your own pay-off.", ]

all_choices = []
for _, s in scenarios.items():
    all_choices.append([f"""You get {s[0][1]}, Person B gets {s[0][0]}""",
                       f"""You get {s[1][1]}, Person B gets {s[1][0]}"""])

task = "You are deciding on allocation for yourself and another person, Person B."

finals = [[]]


def run_experiment_charness_rabin():
    model = Model()
    experiment = Experiment()

    for c in all_choices:
        experiment.add_round(task=task, choices=c)

    endowments = Endowments()
    endowments.set_parameter(parameters=parameters,
                             description="Personality", name="personality")

    experiment.add_subjects(endowments)

    prompts = experiment.generate_experiment_prompt()

    for p in prompts:
        print("-----------------------------------------------")
        print(p)
        print([i["choice_text"] for i in model.run_prompt(p)])
        if len(finals[-1]) >= len(scenarios):
            finals.append([])
        finals[-1].extend([i["choice_text"] for i in model.run_prompt(p)])

    print(finals)
