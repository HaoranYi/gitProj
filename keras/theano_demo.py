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

print('scanning; reusing prev result ...')
def step(m_row, cumulative_sum):
    return m_row + cumulative_sum
M = T.matrix('X')
s = T.vector('s')
output, updates = scan(fn=step, 
                       sequences=[M],
                       outputs_info=[s])
f = function(inputs=[M, s],
             outputs=output,
             updates=updates)
M_value = np.arange(9).reshape(3,3).astype(theano.config.floatX)
s_value = np.zeros((3,), dtype=theano.config.floatX)
print(f(M_value, s_value))

print('scanning; reusing multiple prev results ...')
def step(fm2, fm1):
    f = fm2 + fm1
    r = f/fm1
    return f, r
f_init = T.fvector()
output_info = [dict(initial=f_init, taps=[-2, -1]),  # recurrent info on f 
               None] # no recurrent info on r
output, updates = scan(fn=step, outputs_info=output_info, n_steps=10)
next_fib_terms = output[0]
ratios_between_terms = output[1]
f = function(inputs=[f_init], outputs=[next_fib_terms, ratios_between_terms],
             updates=updates)
out=f([1,1])
print(out[0])
print(out[1])

print('order of argument to the step function:')
print('\telement from first seq ... element from last seq') 
print('\tfirst requested tap from first recurrent ouput') 
print('\tlast requested tap from first recurrent ouput') 
print('\t...') 
print('\tfirst requested tap from last recurrent ouput') 
print('\tlast requested tap from last recurrent ouput') 
print('\tfirst non-sequence')
print('\tlast non-sequence')

print('computing a polynomial ...')
coefficients = T.vector("coefficients")
x = T.scalar('x')
max_coefficients_supported = 1000
def step(coeff, power, free_var):
    return coeff * (free_var**power)
full_range = tensor.arange(max_coefficients_supported)
components, updates = theano.scan(fn=step,
                                  outputs_info=None,
                                  sequences=[coefficients, full_range],
                                  non_sequences=x)
polynomial = components.sum()
calculate_polynomial = function(inputs=[coefficients, x],
                                outputs=polynomial,
                                updates=updates)
test_coeff = np.asarray([1, 0, 2], dtype=theano.config.floatX)
print(calculate_polynomial(test_coeff, 3))

print('computing A^k ...')
k = T.iscalar('k')
A = T.vector('A')
result, updates = scan(fn=lambda prior_result, A: prior_result*A,
                       outputs_info=T.ones_like(A),
                       non_sequences=A,
                       n_steps=k)
final_result=result[-1]
power = function(inputs=[A,k], outputs=final_result, updates=updates)
print(power(range(10),2))
print(power(range(10),4))


print('shared variable')
a = shared(1)
values, updates = scan(lambda: {a:a+1}, n_steps=10)
b = a + 1
c = updates[a] + 1
f = function([], [b, c], updates=updates)
print(b)
print(c)
f()
print(a.get_value())


print('repeat-until ...')
def power_of_2(previous_power, max_value):
    return previous_power*2, scan_module.until(previous_power*2>max_value)
max_value = T.scalar()
values, _ = scan(power_of_2,
                 outputs_info = T.constant(1.),
                 non_sequences = [max_value],
                 n_steps = 1024)
f = function([max_value], values)
print(f(63))


print('''
scanning is loop unrolling. but it is much slower. Because of loop
carried dependencies, it is not running in parallel. Use vectorized
computation is much faster. '''
)

print('scanning: computing tanh(x(t).dot(W)+b) elementwise')
X = T.matrix('X')
W = T.matrix('W')
b_syn = T.vector('b_sym')
results, updates = scan(lambda v: T.tanh(T.dot(v, W) + b_sym), sequences=X)
compute_elementwise = function(inputs=[X, W, b_sym], outputs=results)
x = np.eye(2, dtype=theano.config.floatX)
w = np.ones((2,2), dtype=theano.config.floatX)
b = np.ones((2), dtype=theano.config.floatX)
b[1] = 2
print(compute_elementwise(x, w, b))
print(np.tanh(x.dot(w)+b))


print('scanning: computing x(t)=tanh(x(t-1).dot(W)+y(t).dot(U)+p(T-t).dot(V))')
X = T.vector('X')
W = T.matrix('W')
b_syn = T.vector('b_sym')
U = T.matrix('U')
Y = T.matrix('Y')
V = T.matrix('V')
P = T.matrix('P')
results, updates = scan(lambda y, p, x_tm1: T.tanh(T.dot(x_tm1, W) + 
                                                   T.dot(y, U) +
                                                   T.dot(p, V)), 
                        sequences=[Y, P[::-1]],
                        outputs_info=[X])
compute_seq = function(inputs=[X, W, Y, U, P, V], outputs=results)
x = np.zeros((2), dtype=theano.config.floatX)
x[1] = 1
w = np.ones((2, 2), dtype=theano.config.floatX)
y = np.ones((5, 2), dtype=theano.config.floatX)
y[0, :] = -3
u = np.ones((2, 2), dtype=theano.config.floatX)
p = np.ones((5, 2), dtype=theano.config.floatX)
p[0, :] = 3
v = np.ones((2, 2), dtype=theano.config.floatX)
print(compute_seq(x, w, y, u, p, v))

x_res = np.zeros((5,2), dtype=theano.config.floatX)
x_res[0] = np.tanh(x.dot(w) + y[0].dot(u) + p[4].dot(v))
for i in range(1, 5):
    x_res[i] = np.tanh(x_res[i-1].dot(w) + y[i].dot(u) + p[4-i].dot(v))
print(x_res)


print('computing norms of rows of x')
X = T.matrix("X")
results, updates = scan(lambda x_i: T.sqrt((x_i ** 2).sum()), sequences=[X])
compute_norm_lines = function(inputs=[X], outputs=results)
x = np.diag(np.arange(1, 6, dtype=theano.config.floatX), 1)
print(compute_norm_lines(x))
# comparison with numpy
print(np.sqrt((x ** 2).sum(1)))


print('computing norms of columns of x')
X = T.matrix("X")
results, updates = scan(lambda x_i: T.sqrt((x_i ** 2).sum()), sequences=[X.T])
compute_norm_cols = function(inputs=[X], outputs=results)
x = np.diag(np.arange(1, 6, dtype=theano.config.floatX), 1)
print(compute_norm_cols(x))
# comparison with numpy
print(np.sqrt((x ** 2).sum(0)))


print('computing trace of x')
X = T.matrix('X')
results, updates = scan(lambda i, j, t_f: T.cast(X[i, j] + t_f, theano.config.floatX),
                       sequences=[T.arange(X.shape[0]), T.arange(X.shape[1])],
                       outputs_info=np.asarray(0., dtype=theano.config.floatX))
result = results[-1]
compute_trace = function(inputs=[X], outputs=result)
x = np.eye(5, dtype=theano.config.floatX)
x[0] = np.arange(5, dtype=theano.config.floatX)
print(x)
print(compute_trace(x))
print(np.diagonal(x).sum())


print('computing x(t)=x(t-2).dot(U)+x(t-1).dot(V)+tanh(x(t-1).dot(W)+b)')
X = T.matrix("X")
W = T.matrix("W")
b_sym = T.vector("b_sym")
U = T.matrix("U")
V = T.matrix("V")
n_sym = T.iscalar("n_sym")
results, updates = theano.scan(lambda x_tm2, x_tm1: T.dot(x_tm2, U) + 
                                                    T.dot(x_tm1, V) + 
                                                    T.tanh(T.dot(x_tm1, W) + 
                                                    b_sym),
                               n_steps=n_sym, 
                               outputs_info=[dict(initial=X, taps=[-2, -1])])
compute_seq2 = theano.function(inputs=[X, U, V, W, b_sym, n_sym], outputs=results)
x = np.zeros((2, 2), dtype=theano.config.floatX) # the initial value must be able to return x[-2]
x[1, 1] = 1
w = 0.5 * np.ones((2, 2), dtype=theano.config.floatX)
u = 0.5 * (np.ones((2, 2), dtype=theano.config.floatX) - np.eye(2, dtype=theano.config.floatX))
v = 0.5 * np.ones((2, 2), dtype=theano.config.floatX)
n = 10
b = np.ones((2), dtype=theano.config.floatX)
print(compute_seq2(x, u, v, w, b, n))
x_res = np.zeros((10, 2))
x_res[0] = x[0].dot(u) + x[1].dot(v) + np.tanh(x[1].dot(w) + b)
x_res[1] = x[1].dot(u) + x_res[0].dot(v) + np.tanh(x_res[0].dot(w) + b)
x_res[2] = x_res[0].dot(u) + x_res[1].dot(v) + np.tanh(x_res[1].dot(w) + b)
for i in range(2, 10):
    x_res[i] = (x_res[i - 2].dot(u) + x_res[i - 1].dot(v) +
                np.tanh(x_res[i - 1].dot(w) + b))
print(x_res)

print('computing jacobina of y=tanh(v.dot(A)) wrt x')
v = T.vector()
A = T.matrix()
y = T.tanh(T.dot(v, A))
results, updates = theano.scan(lambda i: T.grad(y[i], v), 
                               sequences=[T.arange(y.shape[0])])
compute_jac_t = theano.function([A, v], results, allow_input_downcast=True) # shape (d_out, d_in)
x = np.eye(5, dtype=theano.config.floatX)[0]
w = np.eye(5, 3, dtype=theano.config.floatX)
w[2] = np.ones((3), dtype=theano.config.floatX)
print(compute_jac_t(w, x))
print(((1 - np.tanh(x.dot(w)) ** 2) * w).T)


print('accumulate a number ...')
print('''
lambda function can return (result, dict(k1=update1, k2=update2)).
''')
k = theano.shared(0)
n_sym = T.iscalar("n_sym")
# results is empty; updates are dicitonary of updates
#results, updates = theano.scan(lambda:{k:(k + 1)}, n_steps=n_sym)
results, updates = theano.scan(lambda: (k+1, {k:(k+1)}), n_steps=n_sym)
accumulator = theano.function([n_sym], results, updates=updates, allow_input_downcast=True)
print(k.get_value())
print(accumulator(5))
print(k.get_value())


print('computing tanh(v.dot(W) + b) * d where d is binomial')
X = T.matrix("X")
W = T.matrix("W")
b_sym = T.vector("b_sym")
trng = T.shared_randomstreams.RandomStreams(1234)
d=trng.binomial(size=W[1].shape)

results, updates = theano.scan(lambda v: T.tanh(T.dot(v, W) + b_sym) * d, 
                               sequences=X)
compute_with_bnoise = theano.function(inputs=[X, W, b_sym], outputs=results,
                          updates=updates, allow_input_downcast=True)
x = np.eye(10, 2, dtype=theano.config.floatX)
w = np.ones((2, 2), dtype=theano.config.floatX)
b = np.ones((2), dtype=theano.config.floatX)
print(compute_with_bnoise(x, w, b))


print('simple random ...')
print('''
If not passing update, the second call will repeat the random number from the
2nd iteration. Passing update will create new random after frist call. Shared
variables are automatically populated in the update dictionary. but you can
populate them in a dictionary
''')
trng = T.shared_randomstreams.RandomStreams(1234)
d = trng.uniform(size=(2,))
results, updates = theano.scan(lambda: d*2, 
                               #sequences=[T.arange(4)],
                               n_steps = 8)
compute_rand = theano.function(inputs=[], outputs=results,
                               updates=updates, allow_input_downcast=True)
print(compute_rand())
print(compute_rand())




