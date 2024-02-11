from datetime import datetime
import pandas as pd
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Tuple


def validate_output(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    Validate the output data from the pipeline
    Args:
        df (pd.DataFrame): output data from the pipeline

    Returns:
        pd.DataFrame: the validated output data
    """
    records: List = df.head().to_dict(orient="records")
    errors: Optional[str] = None
    try:
        SalesOutputDataSchema(outputs=records)
    except ValidationError as e:
        errors = e.json()
    return df, errors


class OutputDataSchema(BaseModel):
    OrderID: Optional[int]
    Product: Optional[str]
    QuantityOrdered: Optional[int]
    PriceEach: Optional[float]
    OrderDate: Optional[datetime]
    PurchaseAddress: Optional[str]
    Sales: Optional[float]
    hour: Optional[int]
    month: Optional[int]
    day: Optional[int]
    day_name: Optional[str]
    year: Optional[int]
    street_name: Optional[str]
    street_number: Optional[str]
    city: Optional[str]


class SalesOutputDataSchema(OutputDataSchema):
    outputs: List[OutputDataSchema]
