from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM


max_features = 12

model = Sequential()
model.add(Embedding(max_features, output_dim=256))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

#import pdb; pdb.set_trace()
for (i, layer) in enumerate(model.layers):
    print(i, type(layer), layer.input_shape, layer.output_shape)

model.summary()    
