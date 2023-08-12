from lightfm import LightFM
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score
from lightfm.datasets import fetch_movielens
import numpy as np

movielens = fetch_movielens(data_home="./")

print(movielens)
train = movielens['train']
test = movielens['test']

#user_data=pd.read_csv("/Users/mac/Downloads/recommendation-pipeline-kedro/movie-recommendation/movielens100k/ml-100k/u.user",delimiter="|",header=None,names=["user_id","age","gender","occupation","zip_code"])
#movies=pd.read_csv("/Users/mac/Downloads/recommendation-pipeline-kedro/movie-recommendation/movielens100k/ml-100k/u.item",sep="|",encoding='latin-1',header=None,names=["movie_id","movie_title","release_date","video_release_date","IMDb_URL","unknown","Action","Adventure","Animation","Children's","Comedy","Crime","Documentary","Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western"])
#ratings=pd.read_csv("/Users/mac/Downloads/recommendation-pipeline-kedro/movie-recommendation/movielens100k/ml-100k/u.data",delimiter="      ",names=["user_id","item_id","rating","timestamp"])

model = LightFM(learning_rate=0.05, loss='bpr')
model.fit(train, epochs=10)

train_precision = precision_at_k(model, train, k=10).mean()
test_precision = precision_at_k(model, test, k=10).mean()

train_auc = auc_score(model, train).mean()
test_auc = auc_score(model, test).mean()

a,_,b,_=dataset.mapping()
a=a.keys()
b=b.keys()

def inference(model,user_id,item_feature,pred_count=5):
    model.predict(user_id,np.arange(len(item_feature)))
    top_items=item_feature[np.argsort(-scores)]
    return top_items[:pred_count]


def sample_recommendations(model,movielens,user_ids):
    print(movielens["train"])
    print("---")
    n_users, n_items = movielens["train"].shape
    for user_id in user_ids:
        known_positives = movielens["item_labels"][movielens["train"].tocsr()[user_id].indices]
        scores = model.predict(user_id, np.arange(n_items))
        top_items = movielens["item_labels"][np.argsort(-scores)]
        print("Known Positives",known_positives[:3])
        print("Top Predictions",top_items[:3])

sample_recommendations(model,movielens,[3,25,451])

