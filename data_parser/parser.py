class Parser:

    def __init__(self, server_data: str, splitters: str = '$|;,()'):
        self.__server_data = server_data

        if self.is_valid_splitters(splitters):
            self.__splitters = splitters
        else:
            raise ValueError('Wrong splitters values: '
                             + 'expected 6 different chars')

    @property
    def server_data(self) -> str:
        return self.__server_data

    @server_data.setter
    def server_data(self, value) -> None:
        if isinstance(value, str):
            self.__server_data = value
        else:
            raise ValueError('Wrong server data format')

    @property
    def splitters(self) -> str:
        return self.__splitters

    @splitters.setter
    def splitters(self, value: str) -> None:
        if self.is_valid_splitters(value):
            self.__splitters = value
        else:
            raise ValueError('Wrong splitters values: '
                             + 'expected 6 different chars')

    @staticmethod
    def is_valid_splitters(value: str) -> bool:
        return all([isinstance(value, str), len(set(value)) == 6,
                   *[not i.isdigit() and not i.isalpha() for i in value]])

    def parsing(self) -> dict:
        data_dict: dict = {}
        for command in self.__server_data.split(self.__splitters[0]):
            name, data = command.split(self.__splitters[1])

            list_data = [[j for j in (i.strip(self.__splitters[4:])
                                      .split(self.__splitters[3]))]
                         for i in data.split(self.__splitters[2])]

            data_dict[name] = self.parse_resourse_data(list_data)

        return data_dict

    @staticmethod
    def parse_resourse_data(data_list: list[list]) -> dict:
        data_dict: dict = {}
        for unit in data_list:
            resource_name, metric, *other = unit
            data_dict.setdefault(resource_name, {})
            data_dict[resource_name].setdefault(metric, []).append(other)

        return data_dict
