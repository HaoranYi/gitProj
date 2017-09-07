from ctypes import *
import struct

# get the C funciton and call it
libc = cdll.msvcrt
print(libc)
libc.printf(b'%d %s\n', 10, b'hello')

# call C function with C string stream
s = create_string_buffer(b'haha', 10)
libc.printf(b'%d %s\n', 10, s)

# pack python object into string stream and call C function with it 
struct.pack_into('ccc', s, 4, b'a', b'b', b'c')
libc.printf(b'%d %s\n', 10, s)
