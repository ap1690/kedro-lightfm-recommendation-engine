import pandas as pd
import numpy as np 
import json
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        return super(NumpyEncoder, self).default(obj)

class MLPredictor:
    def __init__(self, model,item_feature,content_metadata):
        self.model = model
        self.item_feature=item_feature
        self.content_metadata=content_metadata
    def predict(self, args_API, context):
        args_API=args_API.to_dict(orient="records")
        scores=self.model.predict(args_API[0]["user_id"],np.arange(len(self.item_feature)))
        top_items=np.array(self.item_feature)[np.argsort(-scores)]
        prediction=top_items[:args_API[0]["num_of_recommendations"]]
        prediction=[self.content_metadata[self.content_metadata.movie_id==i]["movie_title"].tolist()[0] for i in prediction]
        return {"prediction": prediction}
def save_predictor(model,dataset_object,content_metadata):
    _,_,item_feature,_=dataset_object.mapping()
    item_feature=list(item_feature.keys())
    predictor = MLPredictor(model,item_feature,content_metadata)
    print(predictor)
    return predictor
