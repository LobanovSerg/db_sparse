from requests import get
from data_parser.processing import DataProcessing as dp


def main():
    url = ('http://localhost:21122/monitoring/infrastructure/using/summary/1')
    info = get(url)
    parsing_data = dp(info.text)
    parsing_data.textfile()


if __name__ == '__main__':
    main()
