from pathlib import Path
from argparse import ArgumentParser

import pandas as pd
from data_loading import loadCsv
from utils.csv_to_dataframe import DataLoader
from utils.db_connector import sqlite_connector


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--csv_path",
        "-cp",
        type=str,
        required=False,
        help="Path to the input config file.",
        default="data/processed_data/sales_2019.csv",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    df = DataLoader(csv_path=args.csv_path).load_data(parse_dates=["OrderDate"])
    db_name = "data/databases/sales.sqlite"
    connector = sqlite_connector(db_name)
    loadCsv.CsvToSqliteWithPandas(connector).load_csv_into_table(table_name="sales_2019", df=df)


if __name__ == "__main__":
    main()
