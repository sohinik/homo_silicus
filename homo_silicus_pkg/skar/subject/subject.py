from skar.subject.endowments import Endowment

preset_parameters = set(["ages", "genders", "races", "incomes", "political", "name"])

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
        self._preset_parameters = preset_parameters.intersection(self._available_parameters)
        self._additional_parameters = list(set(
            self._available_parameters) - preset_parameters)

    def set_endowment(self, endowment):
        self._endowment = endowment

    def generate_endowment_prompt(self):
        '''
        Generate prompt outlining subject endoment, including personality and additionally
        provided parameters
        '''
        endowment_prompt = ""
        a_params = self._available_parameters
        endowment = self._endowment.get_endowment()

        # Currently supported automatically: preset_parameters (global var, above)
        if len(a_params) == 0:
            return endowment_prompt
        else:
            all_p = []
            income_p, name_p = "", ""
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
            if "name" in a_params:
                if endowment["name"] == True:
                    name_p = f""" named Subject {self._id}"""
                elif endowment["name"] != False:
                    name_p = f""" named {endowment["name"]}"""
                else:
                    name_p = "person"
                

            # Combine all preset parameters into prompt
            endowment_prompt = ""
            if len(self._preset_parameters) > 0:
                endowment_prompt = f"""You are a {", ".join(all_p)}{" " if len(all_p) > 0 else "person"}{name_p}{income_p}. """

            # Additional parameters must be provided as full sentences, to be appended at the end
            for a in self._additional_parameters:
                endowment_prompt += endowment[a]

        return endowment_prompt
