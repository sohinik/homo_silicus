import random
from skar.experiment.experiment import Experiment
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import Endowments

# Generate set number of subject with randomized views, add to list as additional parameters
num_views = 10
def generate_view():
    heads = random.choice([True, False])
    if heads:
        option1, option2 = "car", "highway"
    else:
        option1, option2 = "highway", "car"
    options = [
        f"{option1} safety is the most important thing.",
        f"{option1} safety is a terrible waste of money; we should only fund {option2} safety.",
        f"{option1} safety is all that matters. We should not fund {option2} safety.",
        f"{option1} safety and {option2} safety are equally important",
        f"{option1} safety is slightly more important thatn {option2} safety",
        f"I don't really care about {option1} safety or {option2} safety"
    ]
    return random.choice(options)

endowment_parameters = []
for i in range(num_views):
    endowment_parameters.append(
        "Your view: " + generate_view())

# Set main task
task = f"""The National Highway Safety Commission is deciding how to allocate its budget between two safety research programs: i) improving automobile safety (bumpers, body, gas tank configurations, seatbelts) and ii) improving the safety of interstate highways (guard rails, grading, highway interchanges, and implementing selective reduced speed limits)."""

# Generate scenarios and choices based on given options
options = (70, 30, 60, 50)
scenarios = [multiple_choice(options, status_quo)
             for status_quo in list(options) + [None]]
all_choices = []

# Helper functions for creating available choices based on "status quo"
def state_status_quo(auto):
    return f"The current budget allocation is {auto}% to auto safety and {100-auto}% to highway safety."

def create_option(auto):
    return f"Allocate {auto}% to auto safety and {100 - auto}% to highway safety"

def create_option_status_quo(status_quo, auto):
    if status_quo > auto:
        return f"Decrease auto program by {status_quo - auto}% of budget and raise the highway program by like amount"
    if status_quo == auto:
        return f"Maintain present budget amounts for the programs"
    if status_quo < auto:
        return f"Decrease the highway program by {auto - status_quo}% of budget and raise the auto program by like amount"

def multiple_choice(options, status_quo):
    transition = ""
    if status_quo:
        transition = state_status_quo(status_quo)
        choices = [create_option_status_quo(
            status_quo, o) for o in options]
    else:
        choices = [create_option(o) for o in options]
    return dict({'transition': transition, 'choices': choices})

# Used for storing final results
finals = [[]]


def run_experiment_samuelson_zeckhauser():
    model = Model()
    experiment = Experiment()

    for s in scenarios:
        choices = s['choices']
        transition = s['transition']
        experiment.add_round(
            task=task, choices=choices, transition=transition, instruction="They are considering the following options:")

    endowments = Endowments()
    endowments.set_parameter(parameters=endowment_parameters,
                             description="Views", name="views")

    experiment.add_subjects(endowments)

    prompts = experiment.generate_experiment_prompt()

    # Run prompts and print corresponding results
    for p in prompts:
        print(p)
        print([i["choice_text"] for i in model.run_prompt(p)])
        print("-----------------------------------------------")
        if len(finals[-1]) >= len(scenarios):
            finals.append([])
        finals[-1].extend([i["choice_text"] for i in model.run_prompt(p)])

    print(finals)
