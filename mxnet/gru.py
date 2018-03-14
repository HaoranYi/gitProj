from __future__ import print_function
import mxnet ast mx
from mxnet import nd, autograd
import numpy as np

mx.random.seed(1)
ctx = mx.gpu(0)

with open("../data/nlp/timemachine.txt") as f:
    time_machine = f.read()

time_machine = time_machine[:-38083]

########################
#  prepare data
########################
character_list = list(set(time_machine))
vocab_size = len(character_list)
character_dict = {}
for e, char in enumerate(character_list):
    character_dict[char] = e
time_numerical = [character_dict[char] for char in time_machine]

def one_hots(numerical_list, vocab_size=vocab_size):
    result = nd.zeros((len(numerical_list), vocab_size), ctx=ctx)
    for i, idx in enumerate(numerical_list):
        result[i, idx] = 1.0
    return result

def textify(embedding):
    result = ""
    indices = nd.argmax(embedding, axis=1).asnumpy()
    for idx in indices:
        result += character_list[int(idx)]
    return result

batch_size = 32
seq_length = 64
# -1 here so we have enough characters for labels later
num_samples = (len(time_numerical) - 1) // seq_length
dataset = one_hots(time_numerical[:seq_length*num_samples]).reshape((num_samples, seq_length, vocab_size))
num_batches = len(dataset) // batch_size
train_data = dataset[:num_batches*batch_size].reshape((num_batches, batch_size, seq_length, vocab_size))
# swap batch_size and seq_length axis to make later access easier
train_data = nd.swapaxes(train_data, 1, 2)

labels = one_hots(time_numerical[1:seq_length*num_samples+1])
train_label = labels.reshape((num_batches, batch_size, seq_length, vocab_size))
train_label = nd.swapaxes(train_label, 1, 2)

########################
#  allocate parameter
########################

num_inputs = vocab_size
num_hidden = 256
num_outputs = vocab_size

########################
#  Weights connecting the inputs to the hidden layer
########################
Wxz = nd.random_normal(shape=(num_inputs,num_hidden), ctx=ctx) * .01
Wxr = nd.random_normal(shape=(num_inputs,num_hidden), ctx=ctx) * .01
Wxh = nd.random_normal(shape=(num_inputs,num_hidden), ctx=ctx) * .01

########################
#  Recurrent weights connecting the hidden layer across time steps
########################
Whz = nd.random_normal(shape=(num_hidden,num_hidden), ctx=ctx)* .01
Whr = nd.random_normal(shape=(num_hidden,num_hidden), ctx=ctx)* .01
Whh = nd.random_normal(shape=(num_hidden,num_hidden), ctx=ctx)* .01

########################
#  Bias vector for hidden layer
########################
bz = nd.random_normal(shape=num_hidden, ctx=ctx) * .01
br = nd.random_normal(shape=num_hidden, ctx=ctx) * .01
bh = nd.random_normal(shape=num_hidden, ctx=ctx) * .01

########################
# Weights to the output nodes
########################
Why = nd.random_normal(shape=(num_hidden,num_outputs), ctx=ctx) * .01
by = nd.random_normal(shape=num_outputs, ctx=ctx) * .01


########################
#  attach gradient
########################
params = [Wxg, Wxi, Wxf, Wxo, Whg, Whi, Whf, Who, bg, bi, bf, bo, Why, by]

for param in params:
    param.attach_grad()

########################
#  define model
########################

def softmax(y_linear, temperature=1.0):
    lin = (y_linear-nd.max(y_linear)) / temperature
    exp = nd.exp(lin)
    partition = nd.sum(exp, axis=0, exclude=True).reshape((-1,1))
    return exp / partition


def gru_rnn(inputs, h, temperature=1.0):
    outputs = []
    for X in inputs:
        z = nd.sigmoid(nd.dot(X, Wxz) + nd.dot(h, Whz) + bz)
        r = nd.sigmoid(nd.dot(X, Wxr) + nd.dot(h, Whr) + br)
        g = nd.tanh(nd.dot(X, Wxh) + nd.dot(r * h, Whh) + bh)
        h = z * h + (1 - z) * g

        yhat_linear = nd.dot(h, Why) + by
        yhat = softmax(yhat_linear, temperature=temperature)
        outputs.append(yhat)
    return (outputs, h)


def cross_entropy(yhat, y):
    return - nd.mean(nd.sum(y * nd.log(yhat), axis=0, exclude=True))

def average_ce_loss(outputs, labels):
    assert(len(outputs) == len(labels))
    total_loss = 0.
    for (output, label) in zip(outputs,labels):
        total_loss = total_loss + cross_entropy(output, label)
    return total_loss / len(outputs)

def SGD(params, lr):
    for param in params:
        param[:] = param - lr * param.grad


def sample(prefix, num_chars, temperature=1.0):
    #####################################
    # Initialize the string that we'll return to the supplied prefix
    #####################################
    string = prefix

    #####################################
    # Prepare the prefix as a sequence of one-hots for ingestion by RNN
    #####################################
    prefix_numerical = [character_dict[char] for char in prefix]
    input = one_hots(prefix_numerical)

    #####################################
    # Set the initial state of the hidden representation ($h_0$) to the zero vector
    #####################################
    h = nd.zeros(shape=(1, num_hidden), ctx=ctx)
    c = nd.zeros(shape=(1, num_hidden), ctx=ctx)

    #####################################
    # For num_chars iterations,
    #     1) feed in the current input
    #     2) sample next character from from output distribution
    #     3) add sampled character to the decoded string
    #     4) prepare the sampled character as a one_hot (to be the next input)
    #####################################
    for i in range(num_chars):
        outputs, h, c = lstm_rnn(input, h, c, temperature=temperature)
        choice = np.random.choice(vocab_size, p=outputs[-1][0].asnumpy())
        string += character_list[choice]
        input = one_hots([choice])
    return string

########################
#  run the model and generate sample text
########################
epochs = 2000
moving_loss = 0.

learning_rate = 2.0

# state = nd.zeros(shape=(batch_size, num_hidden), ctx=ctx)
for e in range(epochs):
    ############################
    # Attenuate the learning rate by a factor of 2 every 100 epochs.
    ############################
    if ((e+1) % 100 == 0):
        learning_rate = learning_rate / 2.0
    h = nd.zeros(shape=(batch_size, num_hidden), ctx=ctx)
    c = nd.zeros(shape=(batch_size, num_hidden), ctx=ctx)
    for i in range(num_batches):
        data_one_hot = train_data[i]
        label_one_hot = train_label[i]
        with autograd.record():
            outputs, h, c = gru_rnn(data_one_hot, h, c)
            loss = average_ce_loss(outputs, label_one_hot)
            loss.backward()
        SGD(params, learning_rate)

        ##########################
        #  Keep a moving average of the losses
        ##########################
        if (i == 0) and (e == 0):
            moving_loss = nd.mean(loss).asscalar()
        else:
            moving_loss = .99 * moving_loss + .01 * nd.mean(loss).asscalar()

    print("Epoch %s. Loss: %s" % (e, moving_loss))
    print(sample("The Time Ma", 1024, temperature=.1))
    print(sample("The Medical Man rose, came to the lamp,", 1024, temperature=.1))
