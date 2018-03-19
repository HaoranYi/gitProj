from blockchain import *

print('----------Encrypt Data------------------------------')
tt = datetime.datetime(2000, 1, 1, 3, 30)
obj = ('ZZZ', 100, tt)
print(obj)

dat = gen_block_data('ZZZ', obj)
print(dat)
print(len(dat))

print('----------Valid Data------------------------------')
obj2 = ('ZZZ', 100, tt)
#dat = '04e09a1f2db092c2505075366f4b78bac11ae128f0316e5291e1d4741901b09c4d4267267e6667da3a9a3c1010e016098def49556c22391deb69800776792f1e65e32d5b1015b0b10517ada62641e13b8bddd2d119b3e3656554e7be9ec3d2a8cd1a7f03e43a4d012317469ecb4b6647d34158a1d9301b3874abc2047e70bb4e'
(r, m) = verify_block_data('ZZZ', obj2, dat)
print(r, m)

print('----------Invalid Data------------------------------')
obj2 = ('ZZZ', 200, tt)
(r, m) = verify_block_data('ZZZ', obj2, dat)
print(r, m)

print('----------Invalid Vendor------------------------------')
obj2 = ('YYY', 200, tt)
(r, m) = verify_block_data('YYY', obj2, dat)
print(r, m)





