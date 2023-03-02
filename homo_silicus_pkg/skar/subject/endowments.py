class Endowments:
    def __init__(self, ages=None, genders=None, races=None, incomes=None, political=None):
        self._parameter_id = 0
        self._ages, self._genders, self._races, self._incomes, self._political = None, None, None, None, None

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

    def increment_parameter_id(self):
        self._parameter_id = self._parameter_id + 1

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

    def set_parameter(self, parameters, description, name=None):
        if not name:
            name = self._parameter_id
            self.increment_parameter_id()

        self._additional_parameters[name] = (description, parameters)

        # if "additional_parameters" not in self._available_parameters:
        #     self._available_parameters["additional_parameters"] = {}
        # self._available_parameters["additional_parameters"][name] = parameters
        self._available_parameters[name] = parameters

    def yield_endowments(self, current_endowment={}, iterated_parameters=[]):
        # print("yield_endowmenets", current_endowment)
        # print("_available_parameters", self._available_parameters)
        # print("len(self._available_parameters)", len(self._available_parameters))
        # print("len(iterated_parameters)", len(iterated_parameters))
        if len(iterated_parameters) == len(self._available_parameters):
            # print("yield_endowmenets 1", current_endowment)
            yield Endowment(current_endowment)
        else:
            next_parameter = list(
                set(self._available_parameters.keys()) - set(iterated_parameters))[0]
            # print("next_parameter", next_parameter)
            iterated_parameters.append(next_parameter)
            for i in self._available_parameters[next_parameter]:
                # print("i", i)
                temp_current_endowment = current_endowment.copy()
                temp_current_endowment[next_parameter] = i
                # print("temp_current_endowment", temp_current_endowment)
                yield from self.yield_endowments(
                    temp_current_endowment, iterated_parameters)

    def get_all_endowments(self):
        return [i for i in self.yield_endowments()]


class Endowment:
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
