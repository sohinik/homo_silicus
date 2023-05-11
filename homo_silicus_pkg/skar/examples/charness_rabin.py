from skar.experiment.experiment import Experiment
from skar.experiment.round import Round
from skar.model import Model
from skar.subject.endowments import Endowments
from skar.results.numbers import *

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

# Additional parameters for subject endowment
endowment_parameters = [
    "",
    "You only care about fairness between players.",
    "You only care about the total pay-off of both players.",
    "You only care about your own pay-off.", ]

# Outline main task
task = "You are deciding on allocation for yourself and another person, Person A."

# Generate choices for each scenario
scenarios = dict({
    "Berk29": ((400, 400), (750, 400)),
    "Berk26": ((0, 800), (400, 400)),
    "Berk23": ((800, 200), (0, 0)),
    "Berk15": ((200, 700), (600, 600)),
    "Barc8": ((300, 600), (700, 500)),
    "Barc2": ((400, 400), (750, 375)),
})
all_choices = []
for _, s in scenarios.items():
    all_choices.append([f"""You get ${s[0][1]}, Person A gets ${s[0][0]}""",
                       f"""You get ${s[1][1]}, Person A gets ${s[1][0]}"""])


def run_experiment_charness_rabin():
    model = Model()
    experiment = Experiment()

    for c in all_choices:
        round_1 = Round(task=task, choices=c, instruction="") # , randomize_choice_ordering=True
        experiment.add_round(round_1)

    endowments = Endowments()
    endowments.set_parameter(parameters=endowment_parameters,
                             description="Personality", name="personality")

    experiment.add_subjects(endowments)

    prompts = experiment.generate_experiment_prompt_useround()

    def run():
        # Used for holding results
        finals = []
        
        # Run prompts and print corresponding results
        for p, r in prompts:
            # print(p)
            # print(model.run_prompt(p, temperature=0, num_choices=5))
            result = model.run_prompt(p, temperature=0, num_choices=5)
            result_all_choice_text = [i["choice_text"] for i in result]
            res = strip_complex(result_all_choice_text[0])
            if not is_number(res):
                print("flagged!", res)
                res = text2int_simple(res)
            prob = 1
            # print(result[0]["choice_raw"]["choices"][0]["logprobs"])
            for i in range(len(result[0]["choice_raw"]["choices"][0]["logprobs"]["tokens"])):
                if result[0]["choice_raw"]["choices"][0]["logprobs"]["tokens"][i].strip() != "":
                    prob = result[0]["choice_raw"]["choices"][0]["logprobs"]["token_logprobs"][i]
            # print(res, "->", r.check_result(res))
            # print("-----------------------------------------------")
            # print(finals)
            finals.append((r.check_result(res), convert_logits(prob)))
        
        return finals

        print(finals)
    
    all_results_randomized = []
    for i in range(50):
        all_results_randomized.append(run())
        print(i)
    
    final_results = all_results_randomized[0]
    final_results_detailed = [[[i[0]], [i[1]]] for i in all_results_randomized[0]]
    for j in range(1, len(all_results_randomized)):
        for k in range(len(all_results_randomized[j])):
            # print(final_results)
            # print(final_results[k])
            # print(final_results[k][0])
            # print(all_results_randomized[j][k][0])
            new_0 = final_results[k][0] + all_results_randomized[j][k][0]
            new_1 = final_results[k][1] + all_results_randomized[j][k][1]
            final_results[k] = (new_0, new_1)
            final_results_detailed[k][0].append(all_results_randomized[j][k][0])
            final_results_detailed[k][1].append('%.3f'%(all_results_randomized[j][k][1]))
            
    print(final_results)
    print(final_results_detailed)
    print([(ii/50, jj/50) for ii, jj in final_results])
    
    #[['1', '1', '0', '1', '0', '1'], ['0', 1, '0', '1', '1', '0'], ['1', '1', '0', 1, '1', '1'], ['1', '1', '0', '1', '1', '1']]

    # Individual prompt -----------------------------------------------------
    # p = [f"""You are a person named Subject 0.

    # You are deciding on allocation for yourself and another person, Person B.

    # 0) You get 600, Person B gets 300
    # 1) You get 500, Person B gets 700

    # What is your choice, with one word: [0, 1]:
    # """]
    # print(p[0])
    # result_1 = model.run_prompt(p, num_choices = len(all_choices))
    # print(result_1)
    # print([i["choice_text"] for i in result_1])
