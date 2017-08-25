from keras.models import Sequential
from keras.layers import Input, Dense,TimeDistributed
from keras.models import Model
from keras.layers import Dense, LSTM, Bidirectional,Masking

inputs = [[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
          [[1,2,3],[4,5,6],[7,8,9],[10,11,12]],
          [[10,20,30],[40,50,60],[70,80,90],[100,110,120]]]

model = Sequential()
model.add(Masking(mask_value=0., input_shape = (4,3)))
model.add(Bidirectional(LSTM(3,return_sequences = True),merge_mode='concat'))
model.add(TimeDistributed(Dense(3,activation = 'softmax')))

#import pdb; pdb.set_trace()
for (i, layer) in enumerate(model.layers):
    print(i, type(layer), layer.input_shape, layer.output_shape)


print("First layer:")
intermediate_layer_model = Model(input=model.input,output=model.layers[0].output)
print(intermediate_layer_model.predict(inputs))
print("")

print("Second layer:")
intermediate_layer_model = Model(input=model.input,output=model.layers[1].output)
print(intermediate_layer_model.predict(inputs))
print("")

print("Third layer:")
intermediate_layer_model = Model(input=model.input,output=model.layers[2].output)
print(intermediate_layer_model.predict(inputs))


print('#######################################################################')
inputs_ = Input(shape=(4,3))
x = Masking(mask_value=0., input_shape = (4,3))(inputs_)
x = Bidirectional(LSTM(3,return_sequences = True),merge_mode='concat')(x)
predictions = TimeDistributed(Dense(3,activation = 'softmax'))(x)
model2 = Model(input=inputs_, output=predictions)

#import pdb; pdb.set_trace()
for (i, layer) in enumerate(model2.layers):
    print(i, type(layer), layer.input_shape, layer.output_shape)

print("First layer:")
intermediate_layer_model = Model(input=model2.input,output=model2.layers[0].output)
print(intermediate_layer_model.predict(inputs))
print("")
print("Second layer:")
intermediate_layer_model = Model(input=model2.input,output=model2.layers[1].output)
print(intermediate_layer_model.predict(inputs))
print("")
print("Third layer:")
intermediate_layer_model = Model(input=model2.input,output=model2.layers[2].output)
print(intermediate_layer_model.predict(inputs))

print('#######################################################################')
from keras import backend as K
inp = model.input
outputs = [layer.output for layer in model.layers]
functors = [K.function([inp]+[K.learning_phase()], [out]) for out in outputs]

layer_outs = [func([inputs, 1.]) for func in functors]
#import pdb; pdb.set_trace()
print(layer_outs)
