from keras import backend as K

inp = model.input
outputs = [layer.output for layer in model.layers]
functors = [K.function([inp]+[K.learning_phase()], [out]) for out in outputs]

# testing
test = np.random.random(input_shape)[np.newaxis,...]
layer_outs = [func([test, 1.]) for func in functors]
print(layer_outs)
