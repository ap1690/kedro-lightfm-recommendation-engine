"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.12
"""

import pandas as pd
import numpy as np 
from lightfm import cross_validation
from lightfm.data import Dataset 
import scipy

def load_data_set() -> pd.DataFrame:
    pass

def perform_data_validation() -> pd.DataFrame:
    pass

def perform_data_cleaning(df):
    df = df.drop_duplicates()
    #df = df.dropna()
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column]=df[column].fillna("")
            # Remove leading/trailing whitespaces from string columns
            df[column] = df[column].str.strip()
            # Normalize string columns to lowercase
            df[column] = df[column].str.lower()
        # Check if the column contains numeric values
        elif pd.api.types.is_numeric_dtype(df[column]):
            df[column]=df[column].fillna(0)
            # Convert numeric columns to appropriate data types
            df[column] = pd.to_numeric(df[column])
        # Check if the column contains datetime values
    return df

def generate_sparse_matrix(user_meta_data,content_meta_data,interactions):
    dataset = Dataset()

    # Buiding Item/User Indecies
    feature_indices = [
    'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
    'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    user_indices = ["m","f"]


    # Buiding Item/User Features

    item_features = []
    for index, row in content_meta_data.iterrows():
        movie_id = row['movie_id']
        features = feature_indices[np.argmax(row[['unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']].tolist())]
        item_features.append(tuple([movie_id,list([features])]))

    user_features = []
    for index, row in user_meta_data.iterrows():
        user_id = row['user_id']
        features = row["gender"]
        user_features.append(tuple([user_id,list([features])]))

    dataset.fit(user_meta_data["user_id"], content_meta_data["movie_id"],item_features=feature_indices,user_features=user_indices)

    # Build the interactions matrix
    interactions_matrix, weights_matrix = dataset.build_interactions([tuple(row) for row in interactions.values])

    # Build the item features matrix
    item_features_matrix = dataset.build_item_features(item_features)

    # Build the user features matrix
    user_features_matrix = dataset.build_user_features(user_features)
    user_id,item_id=interactions_matrix.nonzero()
    return interactions_matrix,item_features_matrix,user_features_matrix,dataset

def perform_train_test_split(interactions_matrix):
    train_set,test_set=cross_validation.random_train_test_split(interactions_matrix,test_percentage=0.2)
    return train_set,test_set




