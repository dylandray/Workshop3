"""
A system that analyze each model and decide if the weight of the model should be updated or not
"""

import os
import pickle
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split



#data processing
df =pd.read_csv("steam.csv", index_col=0)

# data processing
df["positive_ratio"] = df["positive_ratings"] / (df["positive_ratings"] + df["negative_ratings"])



def load_pkl_model(model_path):
    """
    Load a model from a .pkl file
    """
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def load_h5_model(model_path):
    """
    Load a model from a .h5 file
    """
    model = tf.keras.models.load_model(model_path)
    return model

def analyze_model(model, foo):
    X = df.drop(columns=["positive_ratio"], axis=1)
    y = df["positive_ratio"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if foo :
        """the model is a pickle model"""
        # Analyze the model
        precision = model.score(X_test, y_test)
    if not foo:
        """the model is a h5 model"""
        # Analyze the model
        precision = model.evaluate(X_test, y_test)
    # Decide if the weight should be updated or not
    return precision
    

# Get the path to the folder containing the models
folder_path = "/C:/Users/charl/Documents/GitHub/Workshop3_Dylan/Python_code/Python_Code"

# List all the files in the folder
files = os.listdir(folder_path)

# Filter the files to only include .pkl and .h5 files
model_files = [file for file in files if file.endswith((".pkl", ".h5"))]

weight = []

# Load each model
for model_file in model_files:
    foo = False
    model_path = os.path.join(folder_path, model_file)
    # Load the model using the appropriate method
    if model_file.endswith(".pkl"):
        model = load_pkl_model(model_path)
        foo = True
    elif model_file.endswith(".h5"):
        model = load_h5_model(model_path)
        foo = False
    # Analyze the model and decide if the weight should be updated or not
    weight.append(analyze_model(model, foo) * 1000)


#given an order in the way we deal with the models, the weight are the precision of each model
# closer to 1 means the model has more weight