from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

data_dim = 16
timesteps = 8
num_classes = 10
batch_size = 32

# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
model.add(LSTM(32, return_sequences=True,
               batch_input_shape=(batch_size, timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32, return_sequences=True, stateful=True))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32, stateful=True))  # return a single vector of dimension 32
model.add(Dense(10, activation='softmax'))

#import pdb; pdb.set_trace()
for (i, layer) in enumerate(model.layers):
    print(i, type(layer), layer.input_shape, layer.output_shape)
