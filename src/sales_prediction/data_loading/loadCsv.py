import sqlite3
import logging

import pandas as pd


class CsvToSqliteWithPandas:
    def __init__(self, connector: sqlite3.Connection, logger: logging.Logger) -> None:
        self.connector = connector
        self.logger = logger

    def load_csv_into_table(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Load a pandas DataFrame into a SQLite table

        Args:
            df (pd.DataFrame): the DataFrame to load
            table_name (str): the name of the table in the SQLite database
        Returns:
            None
        """
        try:
            self.logger.info(f"Loading data to {table_name} ...")
            with self.connector as connection:
                df.to_sql(
                    name=table_name, con=connection, if_exists="replace", index=False
                )
            self.logger.info(f"Loading data to {table_name} OK")
        except Exception as e:
            self.logger.error(f"Error loading data into table '{table_name}': {e}")
