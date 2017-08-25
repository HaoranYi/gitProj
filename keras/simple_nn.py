from keras.models import Sequential
from keras.layers import Dense
import numpy

numpy.random.seed(7)

dataset = numpy.loadtxt("pima-indians-diabetes.data", delimiter=",")

# split into input (X) and output (Y) variables
X = dataset[:,0:8]   # nSample x 8
Y = dataset[:,8]     # nSample x 1

# create model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))  # 12 neurons; weights 8 x 12
model.add(Dense(8, activation='relu'))  # 8 neurons; weights 12 x 8
model.add(Dense(1, activation='sigmoid')) # weights 8 x 1

# Compile model
# logloss = -t*ln(p) - (1-t)*ln(1-p)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
