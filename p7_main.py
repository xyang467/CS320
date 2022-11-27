# project: p7
# submitter: xyang467
# partner: none
# hours: 2
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import  LogisticRegression
from sklearn.preprocessing import StandardScaler
        
class UserPredictor:
    def __init__(self):
        self.xcols = ['past_purchase_amt','seconds','url','age']
        self.pipe = Pipeline([
            ("poly", PolynomialFeatures(degree=2)),
            ("std", StandardScaler()),
            ("lr", LogisticRegression(max_iter=500)),
        ])
    def fit(self,train_users,train_logs, train_y):
        train_seconds = train_logs.groupby('user_id').sum()
        train_count = train_logs[['user_id','url']].groupby('user_id').count()
        self.train = train_users.join(train_seconds, on='user_id').join(train_count, on='user_id').replace(np.nan, 0).join(train_y.set_index('user_id'), on='user_id')
        self.pipe.fit(self.train[self.xcols], self.train["y"])
    def predict(self,test_users, test_logs):
        test_seconds = test_logs.groupby('user_id').sum()
        test_count = test_logs[['user_id','url']].groupby('user_id').count()
        self.test = test_users.join(test_seconds, on='user_id').join(test_count, on='user_id').replace(np.nan, 0)
        return self.pipe.predict(self.test[self.xcols])
        