from skar.classes.survey import Surveys
from skar.model import Model
from skar.subject.endowments import Endowments

# Set model
model = Model()

# Additional parameters for subject endowment
endowment_parameters = [
    "",
    "You only care about your own pay-off.", ]

endowments = Endowments()
endowments.set_parameter(parameters=endowment_parameters,
                         description="Personality", name="personality")

# Outline main task
task = "You are deciding on allocation for yourself and another person, Person B."

# Generate choices for each scenario
scenarios = dict({
    "Berk29": ((400, 400), (750, 400)),
    "Barc2": ((400, 400), (750, 375)),
})
all_choices = []
for _, s in scenarios.items():
    all_choices.append([f"""You get ${s[0][1]}, Person B gets ${s[0][0]}""",
                       f"""You get ${s[1][1]}, Person B gets ${s[1][0]}"""])


def run_experiment_charness_rabin():
    survey = Surveys([model], endowments, tasks=task, choices=all_choices,
                     one_word=True, temperatures=[0], logprobs=3)

    # results = survey.run_all_write_data(additional_tables=["endowment", "temperature"])
    
    survey.to_json("../homo_silicus_pkg/skar/examples/charness_rabin_survey.json")
