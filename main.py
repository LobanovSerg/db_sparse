from data_parser.processing import DataProcessing as dp


def main():
    info = input()
    parsing_data = dp(info, 'dec')
    parsing_data.textfile()


if __name__ == '__main__':
    main()
