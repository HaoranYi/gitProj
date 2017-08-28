from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers.wrappers import TimeDistributed, Bidirectional

model = Sequential()
model.add(Bidirectional(LSTM(10, return_sequences=True), input_shape=(5,10)))   # both forward and backward propergation
model.add(Bidirectional(LSTM(10)))
model.add(Dense(5))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

model.summary()


