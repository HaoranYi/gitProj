from theano import *
import theano.tensor as T

a = T.dscalar()          # declare variable
b = T.dscalar()
c = a + b                # build expression
f = function([a, b], c)  # compile expr to function
print(f(1.5, 2.5))       # call the function

x = T.dmatrix()
y = T.dmatrix()
z = x + y
f = function([x, y], z)
print(f([[1,2],[3,4]], [[10,20],[30,40]]))

# scalar, vector, matrix, tensor3, tensor4, tensor5

a = T.vector() # declare variable
out = a + a ** 10               # build symbolic expression
f = theano.function([a], out)   # compile function
print(f([0, 1, 2]))
