# Create a LSTM model here
import tensorflow as tf
from keras import layers, models

class NeuralNet(tf.keras.Model):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = layers.Dense(hidden_size, input_shape=(input_size,), activation='relu')
        self.l2 = layers.Dense(hidden_size, activation='relu')
        self.l3 = layers.Dense(num_classes)
    
    def call(self, x):
        x = self.l1(x)
        x = self.l2(x)
        x = self.l3(x)
        return x
