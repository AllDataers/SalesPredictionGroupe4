import pandas as pd
from pathlib import Path


class DataLoader:
    """
    Loads data from a URL.
    """

    def __init__(self, csv_path: str = "", delimiter: str = ",") -> None:
        self._csv_path: Path = Path(csv_path)
        self.delimiter: str = delimiter

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path, delimiter=self.delimiter)
        return df

    @property
    def csv_path(self) -> Path:
        return self._csv_path

    @csv_path.setter
    def csv_path(self, path: str) -> None:
        self._csv_path = Path(path)
