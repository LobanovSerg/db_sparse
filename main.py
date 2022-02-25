from data_parser.processing import DataProcessing as dp


def main():

    db_creds = {'database': 'postgres', 'user': 'postgres',
                'password': 'q1w2e3', 'host': 'localhost', 'port': 5432}

    parsing_data = dp(db_creds)
    parsing_data.textfile()


if __name__ == '__main__':
    main()
