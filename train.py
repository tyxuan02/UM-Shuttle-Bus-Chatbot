# Train the model using the training data
import numpy as np
import json

import tensorflow as tf
from keras import layers, models, optimizers, losses

from nlp_utils import bag_of_words, tokenize, stem

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
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

# stem and lower each word
ignore_words = ['?', '.', '!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
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
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)
print(input_size, output_size)

class NeuralNet(tf.keras.Model):
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNet, self).__init__()
        self.dense1 = layers.Dense(hidden_size, activation='relu', input_shape=(input_size,))
        self.dense2 = layers.Dense(hidden_size, activation='relu')
        self.dense3 = layers.Dense(output_size)

    def call(self, x):
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        return x

model = NeuralNet(input_size, hidden_size, output_size)
model.compile(optimizer=optimizers.Adam(learning_rate=learning_rate),
              loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Create a tf.data.Dataset
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
train_dataset = train_dataset.shuffle(len(X_train)).batch(batch_size)

# Training loop
for epoch in range(num_epochs):
    for step, (words, labels) in enumerate(train_dataset):
        with tf.GradientTape() as tape:
            outputs = model(words, training=True)
            loss = model.compiled_loss(labels, outputs)
        gradients = tape.gradient(loss, model.trainable_variables)
        model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss:.4f}')

print(f'final loss: {loss:.4f}')

# Save the model and training data
model.save('chat_model', save_format='tf')

data = {
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

with open('data.json', 'w') as f:
    json.dump(data, f)

print('training complete. file saved to chat_model.h5 and data.json')
