from skar.classes.conjoint import Conjoint
from skar.model import Model
from skar.subject.endowments import Endowments

# Set model
model = Model()

# Additional parameters for subject endowment
endowment_parameters = [
    "You love ice cream.",
    "You hate ice cream.", ]

endowments = Endowments(name=["Roselia", "Naroli"])
endowments.set_parameter(parameters=endowment_parameters,
                         description="Personality", name="personality")

# Outline main task
task = "You are deciding what type of ice cream to get."

# Generate choices
all_choices = [["chocolate", "vanilla", "mushroom", "strawberry"],
               ["too crunchy to eat nicely", "creamy"],
               ["salty", "bitter", "disgusting - don't pick this one", "sweet"]]


def run_ice_cream():
    survey = Conjoint([model], endowments, len_choices=2, tasks=task, choices=all_choices,
                     one_word=True, temperatures=[0], get_logprobs=3)

    print(survey.run_all())
