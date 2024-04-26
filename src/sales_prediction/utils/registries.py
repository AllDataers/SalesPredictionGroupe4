from sktime.utils import mlflow_sktime


class ModelRegistry:
    @staticmethod
    def load_model(name: str):
        return mlflow_sktime.load_model(name)

    @staticmethod
    def save_model(model, name: str):
        mlflow_sktime.save_model(model, name)
