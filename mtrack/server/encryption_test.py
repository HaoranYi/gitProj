from encryption import *
from data import get_vendor
import datetime
import binascii


print('---------- Vendor ------------------------------')
vendor = get_vendor('AAA')
print(vendor)
print(vendor.uniqid)
print(len(vendor.uniqid))
print(type(vendor.uniqid))


t = vendor.uniqid.encode()
print(len(t))     #32 byte
print(type(t))

#tt = datetime.datetime.now()
tt = datetime.datetime(2000, 1, 1, 3, 30)
print('----------Encrypt Data------------------------------')
obj = ('ZZZZ', 100, tt)
print(obj)

enc_data = encrypt(vendor, obj)
print(enc_data)   #128 byte
print(len(enc_data[0]))
h = b''
for x in enc_data:
  h += binascii.hexlify(x)
print(h)

print('----------Valid Data------------------------------')
obj2 = ('ZZZZ', 100, tt)
print(obj2)
h= '28d21221e263dd03a01f439dd1996904e9252a2e397071f6246e6cda03ccdcd0aa24ed8a46cedc82d771250798c7330b816a379e54172d8ca70295fc30dafcb61ea3ad800bfcbcf5ed351bdb89032fd9ce4bb53a705f16be81155fdcc77a08b44970f6e4c9f9ebc17989a452436d9960d769356329c68f264beb22a99f38e7d1'
enc_data2 = binascii.unhexlify(h)
(uuid, sig)= decrypt(vendor, enc_data2)
print(vendor.uniqid)
print(uuid.decode())
print(vendor.uniqid.encode() == uuid)

sig2 = gen_signature(obj2)
print(sig2)
print(len(sig))  #32 byte
print(sig2==sig)


print('----------False Data------------------------------')
obj3 = ('ZZZZ', 101, tt)
sig3 = gen_signature(obj3)
print(sig3)
print(len(sig3))  #32 byte
print(sig3==sig)

