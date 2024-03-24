class TuningHyperParamsJob:
    def __init__(self, forecaster):
        self.forecaster = forecaster

    def run(self):
        self.forecaster.tune_hyperparameters()