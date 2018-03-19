import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request
from blockchain import *
from crossdomain import *
import json

# Instantiate the app
app = Flask(__name__)

REQUIRED = ['vendor', 'produce', 'quantity', 'date']

def obj2array(values):
  if not all(k in values for k in REQUIRED):
    return 'Missing values', 400
  vendor = values['vendor']
  return [values[n] for n in REQUIRED]

@app.route('/sign', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'],
    headers="Content-Type, Access-Control-Allow-Headers")
def sign():
  jj = request.get_json()
  if isinstance(jj, str):
    values = json.loads(request.get_json())
  else:
    values = jj
  REQUIRED = ['vendor', 'quantity', 'date']
  if not all(k in values for k in REQUIRED):
    return 'Missing values', 400
  vendor = values['vendor']
  obj = obj2array(values)

  sign = gen_block_data(vendor, obj)
  response = {'signature': sign.decode() }
  return jsonify(response), 201

@app.route('/verify', methods=['POST', 'OPTIONS'])
#@crossdomain(origin="*", methods=['POST', 'OPTIONS'])
def verify():
  values = json.loads(request.get_json())

  required = ['vendor', 'signature', 'obj']
  if not all(k in values for k in required):
    return 'Missing values', 400
  vendor = values['vendor']
  signature = values['signature']
  obj = obj2array(values['obj'])

  (res, msg) = verify_block_data(vendor, obj, signature)
  response = {'result': res, 'message': msg }
  return jsonify(response), 201


if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
  args = parser.parse_args()
  port = args.port

  app.run(host='0.0.0.0', port=port, debug=True)
