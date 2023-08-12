"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import perform_data_cleaning,generate_sparse_matrix,perform_train_test_split
import scipy

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=perform_data_cleaning,
            inputs="raw_user_meta_data",
            outputs="cleaned_user_meta_data",
            name="node_clean_user_meta_data"
            ),
        node(
            func=perform_data_cleaning,
            inputs="raw_content_meta_data",
            outputs="cleaned_content_meta_data",
            name="node_clean_content_meta_data"
            ),
        node(
            func=perform_data_cleaning,
            inputs="raw_user_action_data",
            outputs="cleaned_user_action_data",
            name="node_clean_user_action_data"
            ),
        node(
            func=generate_sparse_matrix,
            inputs=["cleaned_user_meta_data", "cleaned_content_meta_data","cleaned_user_action_data"],
            outputs=["interaction_matrix", "item_features_matrix","user_features_matrix","dataset_object"],
            name="node_generate_sparse_matrix"
            ),
        node(
            func=perform_train_test_split,
            inputs="interaction_matrix",
            outputs=["training_interactions_set", "testing_interactions_set"],
            name="node_train_test_split"
            ),
    ])

