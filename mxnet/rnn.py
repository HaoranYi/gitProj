from __future__ import print_function
import mxnet ast mx
from mxnet import nd, autograd
import numpy as np

mx.random.seed(1)
ctx = mx.gpu(0)

with open("../data/nlp/timemachine.txt") as f:
    time_machine = f.read()

print(time_machine[0:500])
print(time_machine[-38075:-37500])
time_machine=time_machine[:-38083]  # chop off legal docs

# char to number
character_list = list(set(time_machine))
vocab_size = len(character_list)
print(character_list)
print('lenght of vocab: %s' % vocab_size)

character_dict = {}
for e, char in enumerate(character_list):
    character_dict[char] = e
print(character_dict)

time_numerical = [character_dict[char] for char in time_machine]
print(len(time_numerical))
print(time_numerical[:20])
print("".join([character_list[idx] for idx in time_numerical[:39]]))

# one-hot encoding
def one_hot(numerical_list, vocab_size = vocab_size):
    result = nd.zeros(len(numerical_list), vocab_size, ctx=ctx)
    for i, idx in enumerate(numerical_list):
        result[i, idx] = 1.0
    return result

def texify(embedding):
    result = ""
    indices = nd.argmax(embedding, axis=1).asnumpy()
    for idx in indices:
        result += character_list[int(idx)]
    return result

seq_lenth = 64
num_samples = (len(time_numerical)-1)//seq_length
dataset = onehot(time_numerical[:seq_length*num_samples]) \
          .reshape((num_samples, seq_length, vocab_size))
texify(dataset[0])

# trainng_data
batch_size = 32
print('# of sequence in dataset: ', len(dataset))
num_batches = len(dataset)//batch_size
print('# of batches: ', num_batches)
train_data = dataset[:num_batches*batch_size].reshape((num_batches,
    batch_size, seq_length, vocab_size))
# swap batch_size and seg_length
train_data = nd.swapaxes(train_data, 1, 2)
print('Shape of data set: ', train_data.shape)

# sanity check
for i in range(3):
    print('***Batch %s: ***\n\n' % (i, texify(train_data[i, :, 0]) +
        texify(train_data[i, :, 1])))


# preparing lables
labels = one_hots(time_numerical[1:seq_length*num_samples + 1])
train_label = labels.reshape((num_batches, batch_size, seq_length, vocab_size))
train_label = nd.swapaxes(train_label, 1, 2)
print('Shape of label: ', train_label.shape)

# sanity check
print(texify(train_data[0,:,0]))
print(texify(train_label[0,:,0]))

# build the neuron network
num_inputs = 77
num_hidden = 256
num_ouputs = 77

########################################
# Weights connecting the inputs to the hidden layer
########################################
Wxh = nd.random_normal(shape=(num_inputs, num_hidden), ctx=ctx)*.01

########################################
# Recurrent Weights connecting hidden layer across time steps
########################################
Whh = nd.random_normal(shape=(num_hidden, num_hidden), ctx=ctx)*.01

########################################
# Bias vector for hidden layer
########################################
bh = nd.random_normal(shape=num_hidden, ctx=ctx)*.01


########################################
# Weights to the output nodes
########################################
Why = nd.random_normal(shape=(num_hidden, num_outputs), ctx=ctx)*.01
by = nd.random_normal(shape=num_outputs, ctx=ctx)*.01


########################################
# attach gradient
########################################
params = [Wxh, Whh, bh, Why, by]
for param in params:
    param.attach_grad()

########################################
# softmax activation
########################################
def softmax(y_linear, temperature=1.0):
    lin = (y_linear - nd.max(y_linear))/temperatore
    exp = nd.exp(lin)
    partition = nd.sum(exp, axis=0, exclue=True).reshape((-1,1))
    return exp/partition


########################################
# with a temperature of 1 (always 1 during training), we get back some set of # probability
########################################
softmax(nd.array([[1, -1], [-1, 1]]), temperature=1.0)


########################################
# if we set a high temperature, we get more entropic (*noiser*) probability
########################################
softmax(nd.array([[1, -1], [-1, 1]]), temperature=100)

########################################
# often we want to sample with a low temperatures to produce sharp probabilities
########################################
softmax(nd.array([[1, -1], [-1, 1]]), temperature=.1)


########################################
# define the model
########################################
def simple_rnn(inputs, state, temperature=1.0):
    outputs = []
    h = state
    for X in inputs:
        h_linear = nd.dot(X, Wxh) + nd.dot(h, Whh) + bh
        h = nd.tanh(h_linear)
        yhat_linear = nd.dot(h, Why) + by
        yhat = softmax(yhat_linear, temperature=temperature)
        outputs.append(yhat)
    return (outputs, h)


########################################
# cross-entropy loss function
########################################
def cross_entropy(yhat, y):
    return - nd.mean(nd.sum(y*nd.log(yhat), axis=0, exclude=True))

cross_entropy(nd.array([.2, .5, .3]), nd.array([1., 0, 0]))


########################################
# averaging the loss over the sequence
########################################
def average_ce_loss(outputs, labels):
    assert(len(outputs)==len(labels))
    total_loss = .0
    for (output, label) in zip(outputs, labels):
        total_loss = total_loss + cross_entropy(output, label)
    return total_loss/len(outputs))


########################################
# optimizer
########################################
def SGD(params, lr):
    for param in params:
        param[:] = param - lr*param.grad


########################################
# generating text by sampling
# for num_chars iterations,
#   1) feed in the current input
#   2) sample next character from output distribution
#   3) add sampled character to the decoded string
#   4) prepare the sampled character as one_hot (to be the next input)
########################################
def sample(prefix, num_chars, temperature=1.0):
    string = prefix
    prefix_numerical = [character_dict[char] for char in prefix]
    input = one_hots(prefix_numerical)
    sample_state = nd.zeros(shape(1, num_hidden), ctx=ctx)
    for i in range(num_chars):
        outputs, sample_state = simple_rnn(input, sample_state, temperature=
                temperature)
        choice = np.random.choice(77, p=outputs[-1][0].asnumpy())
        string += character_list[choice]
        input = one_hots([choice])
    return string


########################################
# training process
########################################
epoch = 2000
moving_loss = 0.0
learning_rate = 0.5
for e in range(epoch):
    ##########################
    # Attenuate the learning rate by a factor of 2 every 100 epochs
    ##########################
    if ((e+1)%100 == 0):
        learning_rate = learning_rate/2.0
    state = nd.zeros(shape=(batch_size, num_hidden), ctx=ctx)
    for i in range(num_batches):
        data_one_hot = train_data[i]
        label_one_hot = train_label[i]
        with autograd.record():
            outputs, state = simple_rnn(data_one_hot, state)
            loss = average_ce_loss(outputs, label_one_hot)
            loss.backward()
        SDG(params, learning_rate)

        ##########################
        # keep a moving average of the losses
        ##########################
        if (i==0) and (e == 0):
            moving_loss = np.mean(loss.asnumpy()[0])
        else:
            moving_loss = .99 * moving_loss + 0.01*np.mean(loss.asnumpy()[0])
    print('Epoch %s. loss: %s' % (e, moving_loss))
    print(sample("The Time ma", 1024, temperature=.1))
    print(sample("The medical man rose, came to the lamp", 1024, temperature=.1))


