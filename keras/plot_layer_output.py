import matplotlib.pyplot as plt
form keras import backend as K

def get_layer_outputs():
    test_image = [....]
    outputs = [layer.output for layer in model.layers]
    comp_graph = [K.function([model.input]+[K.learning_phase()],[output]) 
                  for output in outputs]

    layer_outputs_list = [f([test_image, 1.]) for f in comp_graph]
    layer_outputs =[]
    for layer_outputs in layer_outputs_list:
        print(layer_output[0][0].shape)
        print('\n-----------------------\n')
        layer_outputs.append(layer_output[0][0])
    return layer_outputs

def plot_layer_outputs(layer_number):
    layer_outputs = get_layer_outputs()
    x_max = layer_outputs[layer_number].shape[0]
    y_max = layer_outputs[layer_number].shape[1]
    n = layer_outputs[layer_number].shape[2]

    L = []
    for i in range(n):
        L.append(np.zeros((x_max, y_max)))

    for i in range(n):
        for x in range(x_max):
            for y in range(y_max):
                L[i][x][y] = layer_outputs[layer_number][x][y][i]

    for img in L:
        plt.figure()
        plt.imshow(img, interpolation='nearest')

