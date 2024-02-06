import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def GenerateModel(evaluate=True):
    df = pd.read_csv('data\steam.csv', index_col=0)
    df["positive_ratio"] = df["positive_ratings"] / (df["positive_ratings"] + df["negative_ratings"])
    df = df[(df['positive_ratings'] + df['negative_ratings']) >= 500]
    X = df.drop(columns=["positive_ratio"], axis=1)
    y = df["positive_ratio"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    if evaluate:
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return model, mse, r2
    
    return model

if __name__ == "__main__":
    model, mse, r2 = GenerateModel()
    print(f"Mean Squared Error: {mse}")
    print(f"R2 Score: {r2}")