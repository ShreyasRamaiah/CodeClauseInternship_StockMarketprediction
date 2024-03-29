# -*- coding: utf-8 -*-
"""Copy of CodeClauseDStask1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OmnbKRPQP7mYeVFsYbQlicdzx0JwOOLj

#CodeClause Data Science Internship Task-1

###STOCK MARKET PREDICTION

Importing necessary libraries:
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')

"""Importing our dataset:"""

df = pd.read_csv('/content/stockmarket.csv')
df.head()

"""Exploratory data analysis:"""

df.shape

df.info()

plt.figure(figsize=(15,5))
plt.plot(df['Close'])
plt.title('Close price.', fontsize=15)
plt.ylabel('Price in dollars.')
plt.show()

"""###The prices of stocks are showing an upward trend as depicted by the plot of the closing price of the stocks.

Since the columns 'Adj Close' and 'Close' have the same values, we drop 'Adj Close' to remove redundant data.
"""

df = df.drop(['Adj Close'], axis=1)

"""Checking if there are null values in the dataset:"""

df.isnull().sum()

"""Creating a new column 'Tomorrow' to store closing price of the stock on next day:"""

df["Tomorrow"] = df["Close"].shift(-1)
df

"""Checking if tomorrow's price is greater than today's price:"""

df["Target"] = (df["Tomorrow"] > df["Close"]).astype(int)
df

"""##Training our Machine Learning model used for the prediction - Random Forest Classifier."""

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)

train = df.iloc[:-100]
test = df.iloc[-100:]

predictors = ["Close", "Volume", "Open", "High", "Low"]
model.fit(train[predictors], train["Target"])

"""Measuring accuracy and precision of the model:"""

from sklearn.metrics import precision_score

preds = model.predict(test[predictors])
preds = pd.Series(preds, index=test.index)
precision_score(test["Target"], preds)

combined = pd.concat([test["Target"], preds], axis=1)
combined.plot()

"""Here, we can see that when our model predicts that the price of the stock goes up the next day, 55.88% of the times the prices actually go up.

Orange indicates our model's prediction and blue indicates what actually happened.

Improving the precision of our model:
"""

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)

    return pd.concat(all_predictions)

model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict_proba(test[predictors])[:,1]
    preds[preds >=.6] = 1
    preds[preds <.6] = 0
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

predictions = backtest(df, model, predictors)

precision_score(predictions["Target"], predictions["Predictions"])