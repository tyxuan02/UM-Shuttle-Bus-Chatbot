# Train the model using the training data
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import json

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from keras import optimizers, losses
from keras import layers
import tensorflow as tf

from nlp_utils import bag_of_words, preprocess_text

with open('intents.json', 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # text preprocessing
        words = preprocess_text(pattern)
        # add to our words list
        all_words.extend(words)
        # add to xy pair
        xy.append((words, tag))

# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words:", all_words)

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: TensorFlow's SparseCategoricalCrossentropy needs integer labels
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 200
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
print(input_size, output_size)

model = Sequential([
    Dense(hidden_size, activation='relu', input_shape=(input_size,)),
    Dense(hidden_size, activation='relu'),
    Dense(output_size, activation='softmax')
])

model.compile(optimizer=optimizers.Adam(learning_rate=learning_rate), loss=losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, epochs=num_epochs, batch_size=batch_size)

# Save the model and training data
model.save('lstm_model.h5')
