from abc import ABC, abstractmethod
import pandas as pd


class FeatureEngineering(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class DateFeatureEngineering(FeatureEngineering):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['OrderDate'] =df.to_datetime(df["OrderDate"], format="%m/%d/%y %H:%M")
        df["hour"] = df["OrderDate"].dt.hour
        df["month"] = df["OrderDate"].dt.month
        df["day"] = df["OrderDate"].dt.day
        df["year"] = df["OrderDate"].dt.year
        return df


class AddressFeatureEngineering(FeatureEngineering):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[["street_name", "street_number", "city", "state", "zip_code"]] = df[
            "address"
        ].str.split(", ", expand=True)
        return df


class FeatureEngineeringPipeline:
    def __init__(self):
        self.feature_engineering_steps = []

    def add_feature_engineering(self, feature_engineering: FeatureEngineering):
        self.feature_engineering_steps.append(feature_engineering)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for feature_engineering in self.feature_engineering_steps:
            df = feature_engineering.transform(df)
        return df
