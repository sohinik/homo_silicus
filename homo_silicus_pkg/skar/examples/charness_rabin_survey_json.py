from skar.classes.survey import Surveys

def run_experiment_charness_rabin():
    survey = Surveys.from_json("../homo_silicus_pkg/skar/examples/charness_rabin_survey.json")
    results = survey.run_all_write_data(additional_tables=["endowment", "temperature"])