from typing import Optional, Tuple, List, Dict
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, ValidationError, validator


class SalesSchema(BaseModel):
    dt: Optional[datetime]
    sales: Optional[float]

    @validator("dt")
    def validate_date(cls, v):
        if isinstance(v, pd.Timestamp):
            return v.to_pydatetime()
        return v


class TimeSeriesSchema(BaseModel):
    outputs: List[SalesSchema]


def validate_time_series(df: pd.Series) -> Tuple[pd.Series, Optional[str]]:
    """
    Validate the output data from the pipeline
    Args:
        df (pd.DataFrame): output data from the pipeline

    Returns:
        pd.DataFrame: the validated output data
    """
    records: Dict[pd.Timestamp, float] = df.head().to_dict()
    errors: Optional[str] = None
    try:
        TimeSeriesSchema(
            outputs=[SalesSchema(dt=dt, sales=sales) for dt, sales in records.items()]
        )
    except ValidationError as e:
        errors = e.json()
    return df, errors
