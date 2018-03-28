from data import *

#add_transaction(1, 1)
#confirm_transaction(1)
#h = get_holds('Vendor_A')
#print(h)

#add_transaction(1, 2)
#r = get_pending_confirm('Vendor_B')
#print(r)

r = get_history_transactions(1)
for x in r:
  print(x)
