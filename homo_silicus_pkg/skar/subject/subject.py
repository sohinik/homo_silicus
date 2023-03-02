from skar.subject.endowments import Endowment


class Subject:
    def __init__(self, id, endowment=Endowment()):
        self._id = id
        self._endowment = endowment
        self._available_parameters = self._endowment.get_available_parameters()
        self._additional_parameters = list(set(
            self._available_parameters) - set(["ages", "genders", "races", "incomes", "political"]))

    def set_endowment(self, endowment):
        self._endowment = endowment

    def generate_endoment_prompt(self):
        endowment_prompt = ""
        a_params = self._available_parameters
        endowment = self._endowment.get_endowment()
        if len(a_params) == 0:
            return endowment_prompt
        else:
            age_p = ""
            gender_p = ""
            race_p = ""
            income_p = ""
            political_p = ""
            if "ages" in a_params:
                age_p = f""", {endowment["ages"]} years old"""
            if "genders" in a_params:
                gender_p = f""", {endowment["genders"]}"""
            if "races" in a_params:
                race_p = f""", {endowment["races"]}"""
            if "incomes" in a_params:
                income_p = f""", earning ${endowment["incomes"]} per year"""
            if "political" in a_params:
                political_p = f""", ${endowment["political"]}"""

            endowment_prompt = f"""You are a person named Subject {self._id}{age_p}{gender_p}{race_p}{income_p}{political_p}. """

            for a in self._additional_parameters:
                endowment_prompt += endowment[a]

        return endowment_prompt
