from typing import Dict, List, Optional, Tuple
import pandas as pd
import logging

from sales_prediction.data_processing.base_features_engineering import FeatureEngineering
from sales_prediction.data_processing.validate_ouput import validate_output
from sales_prediction.utils.logger import Logging
from sales_prediction.utils.load_config import load_config


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
        df["Hour"] = df[self.date_column_name].dt.hour
        df["Month"] = df[self.date_column_name].dt.month
        df["Day"] = df[self.date_column_name].dt.day
        df["DayName"] = df[self.date_column_name].dt.day_name()
        df["Year"] = df[self.date_column_name].dt.year
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
                    "StreetAddress", "CityName", "ZipAddress",
                ]
        self.target_columns: List[str] = target_columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        splits = df[self.address_column_name].str.split(self.delimiter, expand=True)
        num_columns = min(len(self.target_columns), splits.shape[1])
        df[self.target_columns[:num_columns]] = splits.iloc[:, :num_columns]
        street_df = df["StreetAddress"].str.split(" ")
        df["StreetName"] = street_df.str[1:].str.join(" ")
        df["StreetNumber"] = street_df.str[0]
        zip_df = df["ZipAddress"].str.split(" ")
        df["ZipCode"] = zip_df.str[1]
        df["StateCode"] = zip_df.str[0]
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

    def __init__(self, feature_engineering_steps: List[FeatureEngineering], logger: logging.Logger) -> None:
        self.feature_engineering_steps: List[
            FeatureEngineering
        ] = feature_engineering_steps
        self.logger = logger

    def transform(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[str]]:

        """
        Performs feature engineering on the input DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to perform feature engineering on.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
        for feature_engineering in self.feature_engineering_steps:
            df = feature_engineering.transform(df)
        validate_df, error = validate_output(df)
        if error:
            self.logger.warning("An error occurred during the dataframe loading.")
        return validate_df, error


if __name__ == "__main__":
    log_dict = load_config("src/config/log.yaml")
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
        ],
        logger=Logging(name="test", log_dict=log_dict).logger,
    )
    final_df, error = pipeline.transform(df)
    print(final_df.head())
