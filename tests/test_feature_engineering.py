import unittest
import sys

sys.path.append('c:/alldaters/salespredictiongroupe4')

import pandas as pd
from src.utils.logger import Logging
from src.data_processing.features_engineering import DateFeatureEngineering
from src.data_processing.features_engineering import AddressFeatureEngineering
from src.data_processing.features_engineering import FeatureEngineeringPipeline

class TestFeatureEngineering(unittest.TestCase):
    def setUp(self):
        # Setup code here (if needed, to prepare the environment before each test)
        self.date_data = {
            "OrderDate": ["01/01/20 10:00", "02/01/20 11:00"],
        }
        self.address_data = {
            "address": [
                "123 Apple St, 101, Cupertino, CA, 95014",
                "456 Banana Ave, 202, Mountain View, CA, 94043",
            ]
        }
        self.df_date = pd.DataFrame(self.date_data)
        self.df_address = pd.DataFrame(self.address_data)

    def test_date_feature_engineering(self):
        # Test DateFeatureEngineering.transform
        transformer = DateFeatureEngineering(date_column_name="OrderDate")
        transformed_df = transformer.transform(self.df_date.copy())
        self.assertTrue("hour" in transformed_df.columns)
        self.assertTrue("month" in transformed_df.columns)
        self.assertTrue("day" in transformed_df.columns)
        self.assertTrue("year" in transformed_df.columns)
        self.assertEqual(transformed_df["hour"].iloc[0], 10)
        self.assertEqual(transformed_df["month"].iloc[0], 1)
        self.assertEqual(transformed_df["day"].iloc[0], 1)
        self.assertEqual(transformed_df["year"].iloc[0], 2020)

    def test_address_feature_engineering(self):
        # Test AddressFeatureEngineering.transform
        transformer = AddressFeatureEngineering(address_column_name="address")
        transformed_df = transformer.transform(self.df_address.copy())
        self.assertTrue("street_name" in transformed_df.columns)
        self.assertTrue("street_number" in transformed_df.columns)
        self.assertTrue("city" in transformed_df.columns)
        self.assertTrue("state" in transformed_df.columns)
        self.assertTrue("zip_code" in transformed_df.columns)
        self.assertEqual(transformed_df["street_name"].iloc[0], "123 Apple St")
        self.assertEqual(transformed_df["street_number"].iloc[0], "101")
        self.assertEqual(transformed_df["city"].iloc[0], "Cupertino")
        self.assertEqual(transformed_df["state"].iloc[0], "CA")
        self.assertEqual(transformed_df["zip_code"].iloc[0], "95014")

    def test_pipeline(self):
        # Test FeatureEngineeringPipeline with both Date and Address feature engineering
        steps = [
            DateFeatureEngineering(date_column_name="OrderDate"),
            AddressFeatureEngineering(address_column_name="address"),
        ]
        pipeline = FeatureEngineeringPipeline(logger=Logging(name="test_pipeline"),
                                              feature_engineering_steps=steps)
        df_combined = pd.concat([self.df_date, self.df_address], axis=1)
        transformed_df, _ = pipeline.transform(df_combined.copy())
        # Check if all expected columns are present
        expected_columns = [
            "hour",
            "month",
            "day",
            "year",
            "street_name",
            "street_number",
            "city",
            "state",
            "zip_code",
        ]
        for column in expected_columns:
            self.assertTrue(column in transformed_df.columns)


if __name__ == "__main__":
    import sys
    print(sys.path)
    unittest.main()
