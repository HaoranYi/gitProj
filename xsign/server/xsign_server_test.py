import requests
import datetime
import json

dat = {
    'vendor': 'ZZZ',
    'produce': 'apple',
    'quantity': 10,
    'date': datetime.datetime(2018, 1, 1, 3, 30).isoformat()
    }

print('-----------------Sign-----------------------')
print(dat)
r = requests.post('http://localhost:5000/sign', json=json.dumps(dat))
sign = json.loads(r.text)
print(sign)


print('-----------------Verify (Valid)-----------------------')
dat2 = {
    'vendor': 'ZZZ',
    'produce': 'apple',
    'signature': sign['signature'],
    'obj': dat
    }
print(dat2)
r = requests.post('http://localhost:5000/verify', json=json.dumps(dat2))
print(r.text)


print('-----------------Verify (invalid data)-----------------------')
dat2 = {
    'vendor': 'ZZZ',
    'signature': sign['signature'],
    'obj': {
      'vendor': 'ZZZ',
      'produce': 'apple',
      'quantity': 11,
      'date': datetime.datetime(2018, 1, 1, 3, 30).isoformat()
      }
    }
print(dat2)
r = requests.post('http://localhost:5000/verify', json=json.dumps(dat2))
print(r.text)


print('-----------------Verify (invalid vendor)-----------------------')
dat2 = {
    'vendor': 'YYY',
    'signature': sign['signature'],
    'obj': {
      'vendor': 'YYY',
      'produce': 'apple',
      'quantity': 11,
      'date': datetime.datetime(2018, 1, 1, 3, 30).isoformat()
      }
    }
print(dat2)
r = requests.post('http://localhost:5000/verify', json=json.dumps(dat2))
print(r.text)
