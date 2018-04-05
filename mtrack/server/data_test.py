from data import *

#add_trans(1, 1)
#confirm_trans(1)
#h = get_holds('Vendor_A')
#print(h)

#add_trans(1, 2)
#r = get_pendings('Vendor_B')
#print(r)

#r = get_trans_history(1)
#for x in r:
#  print(x)

#confirm_trans(1)

#x = add_trans_encrypt(1,1)
#print(x)
#
#y=confirm_trans_decrypt(1)
#print(y)

z = get_encrypt_data(1)
print(z)

y=confirm_trans_decrypt(1, z['data'])
print(y)


