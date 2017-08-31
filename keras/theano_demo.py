from theano import *
import theano.tensor as T
import numpy as np
import time

print("Adding two scalars ...")
a = T.dscalar()          # declare variable
b = T.dscalar()
c = a + b                # build expression
f = function([a, b], c)  # compile expr to function
print(f(1.5, 2.5))       # call the function


print("Adding two matrix ...")
x = T.dmatrix()
y = T.dmatrix()
z = x + y
f = function([x, y], z)
print(f([[1,2],[3,4]], [[10,20],[30,40]]))

# types: scalar, vector, matrix, tensor3, tensor4, tensor5

print("Adding element-wise computation ...")
a = T.vector() # declare variable
out = a + a ** 10               # build symbolic expression
f = theano.function([a], out)   # compile function
print(f([0, 1, 2]))

print("Logistic function")
x = T.dmatrix('x')
s = 1/(1+T.exp(-x))
logistic = function([x], s)
print(logistic([[0, 1],[-1, -2]]))
s2 = (1 + T.tanh(x/2))/2
logistic2 = function([x], s2)
print(logistic2([[0, 1],[-1, -2]]))

print("Computing more than one thing at the same time ...")
a, b = T.dmatrices('a', 'b')
diff = a - b
abs_diff = abs(a - b)
diff_sq = diff**2
f = function([a, b], [diff, abs_diff, diff_sq])
for x in f([[1,1],[1,1]], [[0,1],[2,3]]):
    print(x)

print("Setting a default value ...")    
x, y = T.dscalars('x', 'y')
z = x + y
f = function([x, In(y, value=1)], z)
print(f(33))
print(f(33, 2))

print("Using shared variable ...")
state = shared(0)
inc = T.iscalar('inc')
accumulator = function([inc], state, updates=[(state, state+inc)])
print(state.get_value())
accumulator(1)
print(state.get_value())
accumulator(300)
print(state.get_value())
state.set_value(-1)
accumulator(3)
print(state.get_value())

print("Replacing shared variable with given ...")
fn = state*2+inc
foo = T.scalar(dtype=state.dtype)
skip_shared = function([inc, foo], fn, givens=[(state, foo)])
print(skip_shared(1, 3))
print(state.get_value())

print("Copying functions ...")
state = shared(0)
inc = T.iscalar('inc')
accumulator = function([inc], state, updates=[(state, state+inc)])
accumulator(10)
print(state.get_value())
new_state = shared(0)
new_accumulator = accumulator.copy(swap={state:new_state})
new_accumulator(100)
print(new_state.get_value())
null_accumulator = accumulator.copy(delete_updates=True)
null_accumulator(9000)
print(state.get_value())

print("Using random numbers ...")
from theano.tensor.shared_randomstreams import RandomStreams
from theano import function
srng = RandomStreams(seed=234)
rv_u = srng.uniform((2,2))
rv_n = srng.normal((2,2))
f = function([], rv_u)
g = function([], rv_n, no_default_updates=True)
nearly_zeros = function([], rv_u+rv_u-2*rv_u)
print(f())
print(f())
print(g())
print(g())
print(nearly_zeros())  # random number drawn from safe function are the same

print("Derivatives ...")
x = T.dscalar('x')
y = x**2
gy = T.grad(y, x)
print(pp(gy))  # print out the grad prior to optimization
f = function([x], gy)
print(pp(f.maker.fgraph.outputs[0]))
print(f(4))

x = T.dmatrix('x')
s = T.sum(1/(1+T.exp(-x)))
gs = T.grad(s, x)
dlogistic = function([x], gs)
print(dlogistic([[0,1],[-1,-2]]))

print('Computing jacobian ...')
x = T.dvector('x')
y = x**2
J, updates = theano.scan(lambda i, y, x : T.grad(y[i], x), sequences=T.arange(y.shape[0]), non_sequences=[y, x])
f = theano.function([x], J, updates=updates)
print(f([4, 4]))

print('Computing hessian ...')
x = T.dvector('x')
y = x**2
cost = y.sum()
gy = T.grad(cost, x)
H, updates = theano.scan(lambda i, gy, x: T.grad(gy[i], x), 
                         sequences = T.arange(gy.shape[0]),
                         non_sequences = [gy, x])
print(f([4,4]))

print('fast jacobian times a vector with R-op and L-op ...')
W = T.dmatrix('W')
V = T.dmatrix('V')
x = T.vector('x')
y = T.dot(x, W)
JV = T.Rop(y, W, V)
f = function([W, V, x], JV)
r = f([[1,1],[1,1]],
      [[2,2],[2,2]],
      [0,1])
print(r)

W = T.dmatrix('W')
V = T.vector('V')
x = T.vector('x')
y = T.dot(x, W)
VJ = T.Lop(y, W, V)
f = function([V, x], VJ)
r = f([2,3],
      [0,1])
print(r)

print('hessian times a vector ...')
x = T.dvector('x')
v = T.dvector('v')
y = T.sum(x**2)
gy = T.grad(y,x)
vH = T.grad(T.sum(gy*v),x)
f = function([x,v], vH)
print(f([4,4], [2, 2]))

Hv = T.Rop(gy, x, v)
f = function([x,v], Hv)
print(f([4,4], [2, 2]))

print('ifelse lazy eval ...')
from theano.ifelse import ifelse
a,b = T.scalars('a', 'b')
x,y = T.matrices('x', 'y')
z_switch = T.switch(T.lt(a,b), T.mean(x), T.mean(y))
z_lazy = ifelse(T.lt(a,b), T.mean(x), T.mean(y))

f_switch = function([a,b,x,y], z_switch, mode=Mode(linker='vm'))
f_lazyifelse = function([a,b,x,y], z_lazy, mode=Mode(linker='vm'))
val1 = 0
val2 = 1
big_mat1= np.ones((10000, 10000))
big_mat2= np.ones((10000, 10000))
n_times = 10
tic = time.clock()
for i in range(n_times):
    f_switch(val1, val2, big_mat1, big_mat2)
print('time for unlazye: ', time.clock()-tic, 's')

tic = time.clock()
for i in range(n_times):
    f_lazyifelse(val1, val2, big_mat1, big_mat2)
print('time for lazye: ', time.clock()-tic, 's')

print('scan ... ')
# defining the tensor variables
X = T.matrix("X")
W = T.matrix("W")
b_sym = T.vector("b_sym")

results, updates = scan(lambda v: T.tanh(T.dot(v, W) + b_sym), sequences=X)
compute_elementwise = function(inputs=[X, W, b_sym], outputs=results)

# test values
x = np.eye(2, dtype=theano.config.floatX)
w = np.ones((2, 2), dtype=theano.config.floatX)
b = np.ones((2), dtype=theano.config.floatX)
b[1] = 2

print(compute_elementwise(x, w, b))

# comparison with numpy
print(np.tanh(x.dot(w) + b))
