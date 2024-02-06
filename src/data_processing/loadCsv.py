import pandas as pd
import sqlite3


class CsvToSqliteWithPandas:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)

    def create_table(self, table_name: str, column_names: list) -> None:
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_names)});"
        self.conn.execute(create_table_query)
        self.conn.commit()

    def load_csv_into_table(self, csv_file: str, table_name: str, column_names: list) -> None:
        try:
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_file}' not found.")
        except Exception as e:
            print(f"Error loading data into table '{table_name}': {e}")

    def close_connection(self) -> None:
        self.conn.close()

if __name__ == "__main__":
    db_name = "my_database.sqlite"
    table_name = "my_table"
    column_names = ["col1", "col2"]  # Specify your column names here

    try:
        csv_loader = CsvToSqliteWithPandas(db_name)
        csv_loader.create_table(table_name, column_names)
        csv_loader.load_csv_into_table("data.csv", table_name, column_names)
        csv_loader.close_connection()
        print(f"Data loaded successfully into table '{table_name}'.")
    except Exception as e:
        print(f"Error: {e}")
