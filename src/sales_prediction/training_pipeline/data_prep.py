from typing import Tuple
import pandas as pd
from sktime.split import temporal_train_test_split


def prepare_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare the data for training

    Args:
        df (pd.DataFrame): The input data

    Returns:
        pd.DataFrame: The prepared data
    """
    df = data.set_index(keys=["OrderDate"])
    y_train, y_test = temporal_train_test_split(y=df["Sales"].resample("D").sum(), test_size=0.15)

    return y_train, y_test
