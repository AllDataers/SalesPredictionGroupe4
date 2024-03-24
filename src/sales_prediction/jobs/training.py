from sales_prediction.training_pipeline.train import BaseTrainingPipeline, ModelEvaluator
from sales_prediction.data_processing.features_engineering import FeatureEngineeringPipeline
from sales_prediction.training_pipeline.data_prep import prepare_data


class TrainingJob:
    def __init__(self, df, train_pipeline: BaseTrainingPipeline,
                 metrics: ModelEvaluator):
        self.train_pipeline = train_pipeline
        self.metrics = metrics
        self.df_train, self.df_test = prepare_data(df)

    def run(self):
        self.train_pipeline.train()

    def evaluate(self):
        self.metrics.evaluate(self.df_test)