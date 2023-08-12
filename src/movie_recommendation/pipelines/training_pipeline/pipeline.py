"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import train_model,evaluate_training_performance,evaluate_test_performance
import scipy

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_model,
            inputs=["training_interactions_set","item_features_matrix","user_features_matrix"],
            outputs="model_object",
            name="node_Train_Model"
            ),
        node(
            func=evaluate_training_performance,
            inputs=["model_object","training_interactions_set","item_features_matrix","user_features_matrix"],
            outputs=["Train_Precision@k","Train_AUC_Score"],
            name="node_Get_Training_Performance"
            ),
        node(
            func=evaluate_test_performance,
            inputs=["model_object","testing_interactions_set","item_features_matrix","user_features_matrix"],
            outputs=["Test_Precision@k","Test_AUC_Score"],
            name="node_Get_Testing_Performance"
            )])