from kedro.pipeline import Pipeline, node

from .nodes import save_predictor


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=save_predictor,
                name="save_predictor",
                inputs=["model_object","dataset_object","cleaned_content_meta_data"],  ### Replace with model's name
                outputs="MLPredictor",
            )
        ]
    )
