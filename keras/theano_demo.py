from theano import *
import theano.tensor as T

a = T.dscalar()          # declare variable
b = T.dscalar()
c = a + b                # build expression
f = function([a, b], c)  # compile expr to function
print(f(1.5, 2.5))       # call the function
