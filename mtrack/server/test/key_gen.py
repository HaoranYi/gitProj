from Crypto.PublicKey import RSA
from Crypto import Random
random_generator = Random.new().read
key1 = RSA.generate(1024, random_generator)
#key2 = RSA.generate(1024, random_generator)

fmt='PEM'

prv_key=key1.exportKey(fmt)
pub_key=key1.publickey().exportKey(fmt)

with open('private.pem', 'wb') as f:
    f.write(prv_key)

with open('public.pem', 'wb') as f:
    f.write(pub_key)


r = key1.publickey().encrypt(b'abcdefg', 32)
r2 = key1.decrypt(r)
print(r)
print(r2)


#pub_key1 = RSA.importKey(pub_key) 
#prv_key1 = RSA.importKey(prv_key) 

with open('private.pem', 'rb') as f:
    prv_key1 = RSA.importKey(f.read())

with open('public.pem', 'rb') as f:
    pub_key1 = RSA.importKey(f.read())



r = pub_key1.encrypt(b'gfedcba', 32)
r2 = prv_key1.decrypt(r)
print(r)
print(r2)
