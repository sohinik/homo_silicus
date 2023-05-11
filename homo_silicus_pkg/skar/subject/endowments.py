class Endowments:
    """
    The Endowments class holds all the available parameters used to set an AI subject's personality.
    An individual AI subject will have some combination of the given attributes.

    Args:
        ages (list of int): Age
        genders (list of str): Gender
        races (list of str): Race
        incomes (list of int or str): Income
        political (list of str): Political alignment
    """

    def __init__(self, ages=None, genders=None, races=None, incomes=None, political=None, name=False):
        self._parameter_id = 0
        self._ages, self._genders, self._races, self._incomes, self._political, self._name = None, None, None, None, None, name

        self._additional_parameters = {}
        self._available_parameters = {}

        if ages:
            self.set_ages(ages)
        if genders:
            self.set_genders(genders)
        if races:
            self.set_races(races)
        if incomes:
            self.set_incomes(incomes)
        if political:
            self.set_political(political)
        if name:
            if name == True:
                self.set_name([name])
            else: self.set_name(name)

    def increment_parameter_id(self):
        self._parameter_id = self._parameter_id + 1

    # Methods to manually set different attributes after initialization

    def set_ages(self, ages):
        self._ages = ages
        self._available_parameters["ages"] = ages

    def set_genders(self, genders):
        self._genders = genders
        self._available_parameters["genders"] = genders

    def set_races(self, races):
        self._races = races
        self._available_parameters["races"] = races

    def set_incomes(self, incomes):
        self._incomes = incomes
        self._available_parameters["incomes"] = incomes

    def set_political(self, political):
        self._political = political
        self._available_parameters["political"] = political

    def set_name(self, name):
        self._name = name
        self._available_parameters["name"] = name

    def set_parameter(self, parameters, description, name=None):
        if not name:
            name = self._parameter_id
            self.increment_parameter_id()

        self._additional_parameters[name] = (description, parameters)

        # if "additional_parameters" not in self._available_parameters:
        #     self._available_parameters["additional_parameters"] = {}
        # self._available_parameters["additional_parameters"][name] = parameters
        self._available_parameters[name] = parameters

    # Methods to get endowments

    def yield_endowments(self, current_endowment={}, iterated_parameters=[]):
        '''
        Recursively yield individual endowments from all available parameters

        Args:
            current_endowment (Endowment or dict): Endowment
            iterated_parameters (list): Parameters that have already been added

        Returns:
            none
        '''
        if len(iterated_parameters) == len(self._available_parameters):
            yield Endowment(current_endowment)
        else:
            next_parameter = list(
                set(self._available_parameters.keys()) - set(iterated_parameters))[0]
            iterated_parameters.append(next_parameter)
            for i in self._available_parameters[next_parameter]:
                temp_current_endowment = current_endowment.copy()
                temp_current_endowment[next_parameter] = i
                yield from self.yield_endowments(
                    temp_current_endowment, iterated_parameters)

    def get_all_endowments(self):
        return [i for i in self.yield_endowments()]


class Endowment:
    """
    The Endowment class holds the parameters used to set an individual AI subject's personality and
    attributes.

    Args:
        endowment (Endowment or dict): Endowment
    """

    def __init__(self, endowment={}):
        self._endowment = endowment
        self._available_parameters = list(endowment.keys())

    def get_endowment(self):
        return self._endowment

    def get_available_parameters(self):
        return self._available_parameters

    def set_endowment(self, endowment):
        self._endowment = endowment
        self._available_parameters = list(self._endowment.keys)
