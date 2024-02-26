import tensorflow as tf
import numpy as np
import pandas as pd


class Charles_model(object):

    def __init__(self) -> None:
        self.model = tf.keras.models.load_model('Python_code\model.h5')
    
    def predict(self, data):
        data = np.array(data)
        prediction = self.model.predict(data)
        return prediction

