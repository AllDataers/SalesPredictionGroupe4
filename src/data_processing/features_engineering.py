from typing import Dict, List, Optional
import pandas as pd

from data_processing.base_features_engineering import FeatureEngineering


class DateFeatureEngineering(FeatureEngineering):
    def __init__(self, date_column_name: str) -> None:
        super().__init__()
        self.date_column_name = date_column_name

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A function that takes a DataFrame as input and adds new columns for hour, month, day, and year based on the date_column_name.
        Parameters:
            - df: pd.DataFrame, the input DataFrame
        Returns:
            - pd.DataFrame, the transformed DataFrame with added columns
        """
        df[self.date_column_name] = pd.to_datetime(
            df[self.date_column_name], format="%m/%d/%y %H:%M"
        )
        df["hour"] = df[self.date_column_name].dt.hour
        df["month"] = df[self.date_column_name].dt.month
        df["day"] = df[self.date_column_name].dt.day
        df["year"] = df[self.date_column_name].dt.year
        return df


class AddressFeatureEngineering(FeatureEngineering):
    def __init__(
        self,
        address_column_name: str,
        target_columns: Optional[List[str]] = None,
        delimiter: str = ", ",
    ) -> None:
        super().__init__()
        self.address_column_name = address_column_name
        self.delimiter = delimiter
        if target_columns is None:
            if target_columns is None:
                target_columns = [
                    "street_name",
                    "street_number",
                    "city",
                    "state",
                    "zip_code",
                ]
        self.target_columns: List[str] = target_columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        splits = df[self.address_column_name].str.split(self.delimiter, expand=True)
        num_columns = min(len(self.target_columns), splits.shape[1])
        df[self.target_columns[:num_columns]] = splits.iloc[:, :num_columns]
        return df


class ColumnRenaming(FeatureEngineering):
    def __init__(self, column_name_dict: Dict[str, str]) -> None:
        """
        Initializes the ColumnRenaming class.

        Args:
            column_name_dict (dict): A dictionary mapping old column names to new column names.
        """
        super().__init__()
        self.column_name_dict: Dict[str, str] = column_name_dict

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns=self.column_name_dict)
        return df


class DataCleaner(FeatureEngineering):
    """
    Cleans the DataFrame by dropping missing values and invalid rows.
    """

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Take a pandas DataFrame and drop rows with missing values, where the 'Product' column has the value 'Product'.
        Args:
            df (pd.DataFrame): the input DataFrame
        Returns:
            - pd.DataFrame: the modified DataFrame
        """
        df = df.dropna()
        indices_to_drop = df[df["Product"] == "Product"].index
        df = df.drop(indices_to_drop)
        return df


class SalesColumnAdder(FeatureEngineering):
    def __init__(
        self, quantity_column: str, price_column: str, sales_column: str = "Sales"
    ):
        """
        Initializes the SalesColumnAdder with dynamic column names.
        Args:
            quantity_column (str): The name of the column containing the quantity.
            price_column (str): The name of the column containing the price.
            sales_column (str, optional): The name of the column to add. Defaults to 'Sales'.
        Returns:
            None
        """
        self.quantity_column: str = quantity_column
        self.price_column: str = price_column
        self.sales_column: str = sales_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a 'Sales' column to the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to add the 'Sales' column to.

        Returns:
            pd.DataFrame: Return the DataFrame with the 'Sales' column
        """
        df[self.sales_column] = df[self.quantity_column] * df[self.price_column]
        return df


class DataTypeConverter(FeatureEngineering):
    def __init__(self, type_map):
        """
        Initializes the converter with a dictionary mapping column names to data types.
        :param type_map: A dictionary where keys are column names and values are the target data types.
        """
        self.type_map = type_map

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for column, dtype in self.type_map.items():
            df[column] = df[column].astype(dtype)
        return df


class FeatureEngineeringPipeline:
    def __init__(self, feature_engineering_steps: List[FeatureEngineering]) -> None:
        self.feature_engineering_steps: List[
            FeatureEngineering
        ] = feature_engineering_steps

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs feature engineering on the input DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to perform feature engineering on.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
        for feature_engineering in self.feature_engineering_steps:
            df = feature_engineering.transform(df)
        return df


if __name__ == "__main__":
    column_to_rename = {
        "Order ID": "OrderID",
        "Quantity Ordered": "QuantityOrdered",
        "Price Each": "PriceEach",
        "Order Date": "OrderDate",
        "Purchase Address": "PurchaseAddress",
    }
    data_types_map = {"QuantityOrdered": "int", "PriceEach": "float"}
    quantity_column = "QuantityOrdered"
    date_column = "OrderDate"
    address_column_name = "PurchaseAddress"
    df = pd.read_csv("data/raw/Sales_April_2019.csv")
    pipeline = FeatureEngineeringPipeline(
        [
            DataCleaner(),
            ColumnRenaming(column_to_rename),
            DataTypeConverter(data_types_map),
            SalesColumnAdder(quantity_column, "PriceEach"),
            DateFeatureEngineering(date_column),
            AddressFeatureEngineering(address_column_name),
        ]
    )
    final_df = pipeline.transform(df)
    print(final_df.head())