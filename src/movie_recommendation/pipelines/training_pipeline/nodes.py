"""
This is a boilerplate pipeline 'training_pipeline'
generated using Kedro 0.18.12
"""
"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.12
"""


import pandas as pd
import numpy as np 
from lightfm import cross_validation
from lightfm.data import Dataset 
from lightfm.evaluation import precision_at_k, auc_score
import scipy
from lightfm import LightFM

def train_model(training_interactions_set,item_features_matrix,user_features_matrix):
    model = LightFM(loss='bpr',learning_rate=0.005,no_components=50)
    model.fit(interactions=training_interactions_set, item_features=item_features_matrix,
            user_features=user_features_matrix, epochs=50, num_threads=4)

    return model

def evaluate_training_performance(model,eval_data,item_features_matrix,user_features_matrix):
    p_at_k=precision_at_k(model, eval_data, item_features=item_features_matrix,user_features=user_features_matrix, k=5).mean()
    auc= auc_score(model, eval_data, item_features=item_features_matrix,user_features=user_features_matrix).mean()
    """
    loss = loss.log_loss(user_ids=eval_data.row, item_ids=eval_data.col,
                                  item_features=item_features_matrix,
                                  user_features=user_features_matrix,
                                  model=model).mean()
    """
    print(p_at_k,auc)
    return p_at_k,auc

def evaluate_test_performance(model,eval_data,item_features_matrix,user_features_matrix):
    p_at_k=precision_at_k(model, eval_data, item_features=item_features_matrix,user_features=user_features_matrix, k=5).mean()
    auc= auc_score(model, eval_data, item_features=item_features_matrix,
                      user_features=user_features_matrix).mean()
    print(p_at_k,auc)
    return p_at_k,auc