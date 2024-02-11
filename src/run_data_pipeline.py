from pathlib import Path
from argparse import ArgumentParser

import pandas as pd
from utils.load_config import load_config
from utils.csv_to_dataframe import DataLoader


from data_processing.features_engineering import FeatureEngineeringPipeline
from data_processing.features_engineering import (
    ColumnRenaming,
    DataCleaner,
    DataTypeConverter,
    SalesColumnAdder,
    DateFeatureEngineering,
    AddressFeatureEngineering,
)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--config_path",
        "-c",
        type=str,
        required=False,
        help="Path to the input config file.",
        default=Path(__file__).parent / "config/data_processing_config.yaml",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config_path)
    column_to_rename = config.get("column_renaming", {}).get("column_name_dict", {})
    data_types_map = config.get("data_types_mapping", {})
    output_path = config.get("data_loader", {}).get("output_path", "")
    sales_column_adder = config.get("sales_column_adder", {})
    quantity_column = sales_column_adder.get("quantity_column", "")
    price_column = sales_column_adder.get("price_column", "")
    address_feature_engineering = config.get("address_feature_engineering", {})
    address_column_name = address_feature_engineering.get("address_column_name", "")
    date_feature_engineering = config.get("date_feature_engineering", {})
    date_column = date_feature_engineering.get("date_column_name", "")
    transformation_pipeline = FeatureEngineeringPipeline(
        [
            DataCleaner(),
            ColumnRenaming(column_to_rename),
            DataTypeConverter(data_types_map),
            SalesColumnAdder(quantity_column, price_column),
            DateFeatureEngineering(date_column),
            AddressFeatureEngineering(address_column_name),
        ]
    )
    csv_files_dir = config.get("data_loader", {}).get("raw_path", "")
    df_list = []
    for csv_file_path in Path(csv_files_dir).glob("*.csv"):
        print(f"Processing file: {csv_file_path}")
        raw_df = DataLoader(csv_file_path).load_data()
        df, _ = transformation_pipeline.transform(df=raw_df)
        df_list.append(df)
    final_df = pd.concat(df_list)
    final_df.to_csv(output_path, index=False)
    print(final_df.dtypes)


if __name__ == "__main__":
    print(Path(__file__).parent)
    main()
