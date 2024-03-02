import unittest
import pandas as pd

from sales_prediction.utils.logger import Logging
from sales_prediction.data_processing.features_engineering import DateFeatureEngineering
from sales_prediction.data_processing.features_engineering import AddressFeatureEngineering
from sales_prediction.data_processing.features_engineering import FeatureEngineeringPipeline
from sales_prediction.utils.load_config import load_config


class TestFeatureEngineering(unittest.TestCase):
    def setUp(self):
        log_dict = load_config("src/config/log.yaml")
        self.logger = Logging(name="test_feature_engineering", log_dict=log_dict).logger
        self.date_data = {
            "OrderDate": ["01/01/20 10:00", "02/01/20 11:00"],
        }
        self.address_data = {
            "Address": [
                "123 Apple St, Cupertino, CA 95014",
                "456 Banana Ave, Mountain View, CA 94043",
            ]
        }
        self.df_date = pd.DataFrame(self.date_data)
        self.df_address = pd.DataFrame(self.address_data)

    def test_date_feature_engineering(self):
        # Test DateFeatureEngineering.transform
        transformer = DateFeatureEngineering(date_column_name="OrderDate")
        transformed_df = transformer.transform(self.df_date.copy())
        self.assertTrue("Hour" in transformed_df.columns)
        self.assertTrue("Month" in transformed_df.columns)
        self.assertTrue("Day" in transformed_df.columns)
        self.assertTrue("Year" in transformed_df.columns)
        self.assertEqual(transformed_df["Hour"].iloc[0], 10)
        self.assertEqual(transformed_df["Month"].iloc[0], 1)
        self.assertEqual(transformed_df["Day"].iloc[0], 1)
        self.assertEqual(transformed_df["Year"].iloc[0], 2020)

    def test_address_feature_engineering(self):
        # Test AddressFeatureEngineering.transform
        transformer = AddressFeatureEngineering(address_column_name="Address")
        transformed_df = transformer.transform(self.df_address.copy())
        print(transformed_df.columns)
        self.assertTrue("StreetName" in transformed_df.columns)
        self.assertTrue("StreetNumber" in transformed_df.columns)
        self.assertTrue("City" in transformed_df.columns)
        self.assertTrue("Ctate" in transformed_df.columns)
        self.assertTrue("ZipCode" in transformed_df.columns)
        self.assertEqual(transformed_df["StreetName"].iloc[0], "123 Apple St")
        self.assertEqual(transformed_df["StreetNumber"].iloc[0], "101")
        self.assertEqual(transformed_df["City"].iloc[0], "Cupertino")
        self.assertEqual(transformed_df["State"].iloc[0], "CA")
        self.assertEqual(transformed_df["ZipCode"].iloc[0], "95014")

    def test_pipeline(self):
        # Test FeatureEngineeringPipeline with both Date and Address feature engineering
        steps = [
            DateFeatureEngineering(date_column_name="OrderDate"),
            AddressFeatureEngineering(address_column_name="Address"),
        ]
        pipeline = FeatureEngineeringPipeline(logger=self.logger,
                                              feature_engineering_steps=steps)
        df_combined = pd.concat([self.df_date, self.df_address], axis=1)
        transformed_df, _ = pipeline.transform(df_combined.copy())
        # Check if all expected columns are present
        expected_columns = [
            "Hour",
            "Month",
            "Day",
            "Year",
            "StreetName",
            "StreetNumber",
            "CityName",
            "StateCode",
            "ZipCode",
        ]
        for column in expected_columns:
            self.assertTrue(column in transformed_df.columns)


if __name__ == "__main__":
    unittest.main()
