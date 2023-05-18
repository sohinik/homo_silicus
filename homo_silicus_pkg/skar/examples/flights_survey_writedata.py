from skar.classes.survey import Surveys
from skar.model import Model
from skar.subject.endowments import Endowments

# Set model
model = Model()

# Additional parameters for subject endowment
endowment_parameters = ["",
                        "You hate flying.",
                        "You tolerate flying.",
                        "You love flying.",
                        ]
ages = [10, 20, 40, 70]

endowments = Endowments(ages=ages)
endowments.set_parameter(parameters=endowment_parameters,
                         description="Flight Preference", name="flight preference")

scenario = "You are taking a jet plane for a business appointment in Paris."
task = "Which flight will you choose?"

all_choices = [["A flight that is often late in arriving in Paris. The flight is nonstop, and it is anticipated that it will be 50% full. Flight attendants are “warm and friendly” and you would have a choice of two movies for entertainment.",
               "A flight that is almost never late in arriving in Paris. The plane will make two intermediate stops, and it is anticipated that the plane will be 90% full. Flight attendants are ‘cold and curt” and a full entertainment system is provided."]]


def run_flights_survey_writedata():
    survey = Surveys([model], endowments, scenarios=scenario, tasks=task, choices=all_choices,
                     one_word=True, temperatures=[0, 1], logprobs=3)

    results = survey.run_all_write_data(additional_tables=["endowment", "temperature"], analyze=True)

    # survey.to_json("../homo_silicus_pkg/skar/examples/flights_survey.json")
