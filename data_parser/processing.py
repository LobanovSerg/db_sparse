from datetime import datetime
from statistics import mean, median

from .parser import Parser


class DataProcessing(Parser):

    @staticmethod
    def parse_resourse_data(data_list: list[list]) -> dict:
        data_dict: dict = {}
        for unit in data_list:
            resource_name, metric, *other = unit
            data_dict.setdefault(resource_name, {})
            (data_dict[resource_name].setdefault(metric, [])
             .append(int(other[-1])))

        for resource in data_dict:
            data_dict[resource] = (DataProcessing.
                                   __calc_values(data_dict[resource]))

        return data_dict

    @staticmethod
    def __calc_values(resource_data: dict) -> dict:
        data_dict = {}
        for metric in resource_data:
            metric_mean = mean(resource_data[metric])
            metric_median = median(resource_data[metric])
            usage_type = (DataProcessing.
                          __usage_type(metric_mean, metric_median))
            intensivity = DataProcessing.__intensivity(metric_median)
            data_dict[metric] = {
                'mean': metric_mean,
                'median': metric_median,
                'usage_type': usage_type,
                'intensivity': intensivity,
                'decision': DataProcessing.__decision(usage_type, intensivity)
            }

        return data_dict

    @staticmethod
    def __usage_type(mean_value: float, median_value: float) -> str:
        return ('Decline' if mean_value < median_value * .75 else
                'Lope' if mean_value > median_value * 1.25 else 'Stable')

    @staticmethod
    def __intensivity(median_value: float) -> str:
        return ('Low' if 0 < median_value <= 30 else
                'Medium' if 30 < median_value <= 60 else
                'High' if 60 < median_value <= 90 else 'Extreme')

    @staticmethod
    def __decision(usage: str, intense: str) -> str:
        values_dict = {
            'DeclineLow': 'delete resource', 'StableLow': 'delete resource',
            'LopeLow': 'delete resource', 'DeclineMedium': 'delete resource',
            'StableMedium': 'normal using', 'LopeMedium': 'normal using',
            'DeclineHigh': 'normal using', 'StableHigh': 'normal using',
            'LopeHigh': 'extend resource', 'DeclineExtreme': 'extend resource',
            'StableExtreme': 'extend resource',
            'LopeExtreme': 'extend resource'
        }
        return values_dict[usage + intense]

    def textfile(self) -> None:
        file_name = (f'report_{str(datetime.now())[:16]}.txt'
                     .replace(' ', '_').replace(':', '-'))

        with open(file_name, 'w') as file:
            file.write(f'- Server Data Report \n- create: {datetime.now()}\n')

            for name, data in self.parsing().items():
                file.write(f'\n\n- {name}\n{"_" * 105}\n')
                file.write('|   resource   |  dimension  |    mean    |')
                file.write('  mediana  |  usage type  |  intensivity  |')
                file.write('     decision     |\n')
                file.write('-' * 105 + '\n')

                for resource, res_data in data.items():
                    for dimention, dim_data in res_data.items():
                        file.write(f'| {resource:13s}| {dimention:12s}|')
                        file.write(f'{str(dim_data["mean"])[:10]:>11s} |')
                        file.write(f'{str(dim_data["median"])[:9]:>10s} |')
                        file.write(f'{dim_data["usage_type"]:>13s} |')
                        file.write(f'{dim_data["intensivity"]:>14s} |')
                        file.write(f'{dim_data["decision"]:>17s} |\n')

                    file.write('-' * 105 + '\n')
