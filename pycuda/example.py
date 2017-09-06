import pycuda.autoinit
import pycuda.driver as drv
import numpy

from pycuda.compiler import SourceModule

# mod is compiled and uploaded onto GPU
mod = SourceModule('''
__global__ void multiply_them(float* dest, float* a, float* b) 
{
    const int i = threadIdx.x;
    dest[i] = a[i]*b[i];
}

''')

multiply_them = mod.get_function("multiply_them")
a = numpy.random.randn(400).astype(numpy.float32)
b = numpy.random.randn(400).astype(numpy.float32)
dest = numpy.zero_like(a)

# numpy arrays are allocated on the GPU device and transferred to the host
# when the computation is completed.
multiply_them(
        drv.Out(dest), drv.In(a), drv.In(b),
        block=(400, 1, 1), grid=(1,1))
#print(dest-a*b)
print(numpy.allclose(dest, a*b))
