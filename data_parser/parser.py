import psycopg2


class Parser:

    def __init__(self, server_data, splitters: str = '$|;,()'):
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
        if isinstance(value, str) or isinstance(value, dict):
            self.__server_data = value
        else:
            raise ValueError('Wrong server data format')

    @property
    def db_request(self) -> str:
        return self.__db_request

    @db_request.setter
    def db_request(self, value) -> None:
        if isinstance(value, str):
            self.__db_request = value
        else:
            raise ValueError('Wrong database request format')

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

        if isinstance(self.__server_data, str):
            for command in self.__server_data.split(self.__splitters[0]):
                name, data = command.split(self.__splitters[1])

                list_data = [[j for j in (i.strip(self.__splitters[4:])
                                        .split(self.__splitters[3]))]
                            for i in data.split(self.__splitters[2])]

                data_dict[name] = self.parse_resourse_data(list_data)

        if isinstance(self.__server_data, dict):
            with psycopg2.connect(**self.__server_data) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        SELECT team, resource, dimension, usage
                        FROM usage_stats.resources
                        ''')

                    for row in iter(cursor.fetchone, None):
                        data_dict.setdefault(row[0], []).append(row[1:])

            for name, data_res in data_dict.items():
                data_dict[name] = self.parse_resourse_data(data_res)

        return data_dict

    @staticmethod
    def parse_resourse_data(data_list: list[list]) -> dict:
        data_dict: dict = {}
        for unit in data_list:
            resource_name, metric, *other = unit
            data_dict.setdefault(resource_name, {})
            data_dict[resource_name].setdefault(metric, []).append(other)

        return data_dict
