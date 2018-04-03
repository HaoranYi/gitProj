import requests
import datetime
import json

print('-----------------all vendors-----------------------')
dat = { }
print(dat)
r = requests.post('http://localhost:5000/vendors', json=json.dumps(dat))
print(r.text)


print('-----------------holds-----------------------')
dat = {
    'name': 'Vendor_A',
    }
print(dat)
r = requests.post('http://localhost:5000/holds', json=json.dumps(dat))
print(r.text)


print('-----------------pendings-----------------------')
dat = {
    'name': 'Vendor_B',
    }
print(dat)
r = requests.post('http://localhost:5000/pendings', json=json.dumps(dat))
print(r.text)

print('-----------------transhistory-----------------------')
dat = {
    'medicine_id': 1,
    }
print(dat)
r = requests.post('http://localhost:5000/transhistory', json=json.dumps(dat))
print(r.text)

print('-----------------addTrans-----------------------')
dat = {
    'hold_id': 1,
    'buyer_id': 3
    }
print(dat)
#r = requests.post('http://localhost:5000/addtrans', json=json.dumps(dat))
print(r.text)

print('-----------------confirmTrans-----------------------')
dat = {
    'hold_id': 1,
    }
print(dat)
#r = requests.post('http://localhost:5000/confirmtrans', json=json.dumps(dat))
#print(r.text)

