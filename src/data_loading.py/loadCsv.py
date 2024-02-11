import sqlite3

import pandas as pd


class CsvToSqliteWithPandas:
    def __init__(self, connector: sqlite3.Connection) -> None:
        self.connector = connector

    def load_csv_into_table(self, df: pd.DataFrame, table_name: str) -> None:
        try:
            with self.connector as connection:
                df.to_sql(table_name, connection, if_exists="replace", index=False)
        except Exception as e:
            print(f"Error loading data into table '{table_name}': {e}")
