""" A collection of examples that demonstrate the usage of function api to
build a deep learning model.

TAKE-AWAYS: layers, models are essentially a function (i.e. callable) that
take an input tensor(s) and return output tensor(s). A model is a graph of
such functions.
"""
from keras.layers import Input, Dense
from keras.models import Model

##############################################################################
# A simple example to use functional api
##############################################################################

# This returns a tensor
inputs = input(shape-(784,))

# A layer instance is callable on a tensor, and return a tensor
x = Dense(64, activation='relu')(inputs)
x = Dense(64, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)

# This create a model that includes the Input layer and three Dense layers.
model = Model(inputs=inputs, outputs=predictions)
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(data, lables)  # starts training

##############################################################################
# Models, like layers, are callable too
##############################################################################
inputs = input(shape-(784,))

# reuse the model defined above, returns the 10-way softmax
y = model(x)

from keras.layers import TimeDistributed

# Input tensor for sequences of 20 timesteps
# each containing a 784-dimension vector
input_sequences = Input(shape=(20, 784))

# This applies our previous model to every timestep in the input sequences.
# the output of the previous model was a 10-way softmax,
# so the output of the layer below will be a sequence of 20 vectors of size 10
processed_sequences = TimeDistributed(model)(input_sequences)

##############################################################################
# multiple-input multiple-output models
##############################################################################
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model

# headline input: meant to received sequences of 100 integers, between 1 and
# 10000. Note that we can name a layer by passing it a "name" argument.
main_input = Input(shape(100,), dtype='int32', name='main_input')

# this embedding layer will encode the input sequence into a sequence of dense
# 512-dimensional vectors.
x = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input)

# A LSTM will transform the vector sequence into a single vector, containing
# informationo of the entire sequence
lstm_out = LSTM(32)(x)

# Here is auxillary loss
auxilary_out = Dense(1, activation='sigmod', name='aux_output')(lstm_out)

auxiliary_input = Input(shape=(5,), name='aux_input')
x = keras.layers.concatenate([lstm_out, auxiliary_out])

# We stack a deep connected network on top of it
x = Dense(64, activate='relu')(x)
x = Dense(64, activate='relu')(x)
x = Dense(64, activate='relu')(x)

# finally we add the main logistic regression layer
main_output = Dense(1, activation='sigmod', name='main_output')(x)

model = Model(inputs=[main_input, auxiliary_input], outptus=[main_output, auxiliary_out])
model.compile(optimizer='rmsprop', loss='binary_corssentropy', loss_weight=[1., .2])
model.fit([headline, additional_data], [labels, labels], epoch=50,
        batch_size=32)

# Or pass a dictionary with variable as the key to specify the model and
# training data
model.complie(optimizer='rmsprop',
              loss = {'main_output':'binary_crossentropy', 'aux_ouput':'binary_crossentropy'},
              loss_weight = {'main_output':1.0, 'aux_ouput':0.2})
model.fit({'main_input':headline_data, 'aux_input':additional_data},
          {'main_ouput':label, 'aux_out':label},
          epochs=50, batch_size=32)

##############################################################################
# shared layer
##############################################################################
"""predict whether two tweets are from the same person """
import keras
from keras.layers import Input, LSTM, Dense
from keras.models import Model

tweet_a = Input(shape=(140, 256))
tweet_b = Input(shape=(140, 256))

# This layer can take input matrix and will return a vector of size 64
shared_lstm = LSTM(64)

# when we reuse the same layer instance multiple times, the weights of the
# layer are also being reused (it is effectively the same layer)
encoded_a = shared_lstm(tweet_a)
encoded_b = shared_lstm(tweet_b)

# concatenate two vectors
merged_vector = keras.layers.concatenate([encoded_a, encoded_b], axis=-1)

# add a logistic regression on top
prediction = Dense(1, activation='sigmod')(merged_vector)

# We define a trainable model linking the tweet inputs into predictors
model = Model(inputs=[tweet_a, tweet_b], outputs=predictions)
model.complie(optimizer='rmsprop', loss = 'binary_crossentropy', metrics=['accuracy'])
model.fit([data_a, data_b], labels, epoch=10)

""" each layer is a node in the computation graph. With shared layer, this
layer will correpond to multiple nodes in the computation graph. To get the
output for each computation, you will need to supply an index.
"""
a = Input(shape(140, 256))
lstm = LSTM(32)
encoded_a = lstm(a)
assert ltsm.output==encoded_a

a = Input(shape(140, 256))
b = Input(shape(140, 256))
lstm = LSTM(32)
encoded_a = lstm(a)
encoded_b = lstm(b)
assert lstm.get_output_at(0)==encoded_a
assert lstm.get_output_at(1)==encoded_b

""" inception module (go deeper with convolution) """
input_img = Input(shape=(256,256,3))
tower_1 = Conv2D(64, (1,1), padding='same', activation='relu')(input_img)
tower_1 = Conv2D(64, (3,3), padding='same', activation='relu')(tower_1)

tower_2 = Conv2D(64, (1,1), padding='same', activation='relu')(input_img)
tower_2 = Conv2D(64, (5,5), padding='same', activation='relu')(tower_2)

tower_3 = MaxPooling2D((3,3), strides=(1,1), padding='same')(input_img)
tower_3 = Conv2D(64, (1,1), padding='same', activation='relu')(tower_2)

output = keras.layers.concatenate([tower_1, tower_2, tower_3], axix=1)

""" residual connection on a convolution layer (deep resudule learning for
image recognition) """
from keras.layers import Conv2D, Input

# input tensor for a 3-channel 256x256 image
x = Input(shape(256,256,3))
# 3x3 conv with 3 output channels (same as input channels)
y = Conv2D(3, (3,3), padding='same')(x)
# this returns x+y
z = keras.layers.add([x,y])  # should be subtract??

""" shared vision model """
from keras.layers import Conv2D, MaxPooling2D, Input, Dense, Flatten
from keras.models import Model

# first, define the vision modules
digit_input = Input(shape(27,27,1))
x = Conv2D(64, (3,3))(digit_input)
x = Conv2D(64, (3,3))(x)
x = MaxPooling2D((2,2))(x)
out = Flatten(x)

vision_model = Model(digit_input, output)

# the tell-digits-apart model
digit_a = Input(shape(27,27,1))
digit_b = Input(shape(27,27,1))

# shared vision model
out_a = vision_model(digit_a)
out_b = vision_model(digit_b)

concatenated = keras.layers.concatenate([out_a, out_b])
out = Dense(1, activation='sigmod')(concatenated)

classification_model = Model([digit_a, digit_b], out)

""" visual question answer model """
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras.layers import Input, LSTM, Embedding, Dense
from keras.models import Model, Sequential

# define a vision model that encode out image to vector
vision_model = Sequential()
vision_model.add(Conv2D(64, (3,3), activation='relu', padding='same', input_shape=(224,224,3)))
vision_model.add(Conv2D(64, (3,3), activation='relu'))
vision_model.add(MaxPooling2D((2,2)))
vision_model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
vision_model.add(Conv2D(128, (3,3), activation='relu'))
vision_model.add(MaxPooling2D((2,2)))
vision_model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
vision_model.add(Conv2D(256, (3,3), activation='relu'))
vision_model.add(Conv2D(256, (3,3), activation='relu'))
vision_model.add(MaxPooling2D((2,2)))
vision_model.add(Flatten())

# let's get a tensor with the output of our vision model
image_input = Input(shape=(224,224,3))
encoded_image = vision_model(image_input)

# define a language model to encode the question into a vector
# each question will be at most 100 words long
# and we will index words as integer from 1 to 9999
question_input = Input(shape=(100,), dtype='int32')
embeded_question = Embedding(input_dim=10000, output_dim=256, input_length=100)(question_input)
encoded_question = LSTM(256)(embeded_question)

# concatenate the question vector with the image vector
merged = keras.layers.concatenate([encoded_question, encoded_image])

# a logistic regression over 1000 words on top
output = Dense(1000, activation='softmax')(merged)

# final model
vqa_model = Model(inputs=[image_input, question_input], output=output)

""" video question answer model """
from keras.layers import TimeDistributed
video_input = Input(shape=(100, 224, 224, 3))

# use vision model to do video frame encoding
encoded_frame_sequence = TimeDistributed(vision_model)(video_input)  # the output will be a sequence of vectors
encoded_video = LSTM(256)(encoded_frame_sequence)  # the output will be a vector

# this is a model-level representation of the question encoder, reusing the
# same weights as before
question_encoder = Model(inputs=question_input, outputs=encoded_question)

# video question answering model
merged = keras.layers.concatenate([encoded_video, encoded_video_question])
output = Dense(1000, activation='softmax')(merged)
video_qa_model = Model(inputs=[video_input, video_question_input], outputs=output)
