from skar.subject.endowments import Endowment


class Subject:
    """
    The Subject class creates a mock AI subject and functionality
    to generate a corresponding prompt with the given attributes.

    Args:
        id (any): Unique identifier for the subject, ex. ID, number, name
        endowment (Endowment): Subject endowment
    """

    def __init__(self, id, endowment=Endowment()):
        self._id = id
        self._endowment = endowment
        self._available_parameters = self._endowment.get_available_parameters()
        self._additional_parameters = list(set(
            self._available_parameters) - set(["ages", "genders", "races", "incomes", "political"]))

    def set_endowment(self, endowment):
        self._endowment = endowment

    def generate_endoment_prompt(self):
        '''
        Generate prompt outlining subject endoment, including personality and additionally
        provided parameters
        '''
        endowment_prompt = ""
        a_params = self._available_parameters
        endowment = self._endowment.get_endowment()

        # Currently supported automatically: age, gender, race, income, political alignment
        if len(a_params) == 0:
            return endowment_prompt
        else:
            all_p = []
            income_p = ""
            if "ages" in a_params:
                all_p.append(f"""{endowment["ages"]} years old""")
            if "genders" in a_params:
                all_p.append(f"""{endowment["genders"]}""")
            if "races" in a_params:
                all_p.append(f"""{endowment["races"]}""")
            if "incomes" in a_params:
                income_p = f""", earning ${endowment["incomes"]} per year"""
            if "political" in a_params:
                all_p.append(f"""{endowment["political"]}""")

            # Combine all given parameters into prompt
            endowment_prompt = f"""You are a {", ".join(all_p)}{" " if len(all_p) > 0 else ""}person named Subject {self._id}{income_p}. """

            # Additional parameters must be provided as full sentences, to be appended at the end
            for a in self._additional_parameters:
                endowment_prompt += endowment[a]

        return endowment_prompt
