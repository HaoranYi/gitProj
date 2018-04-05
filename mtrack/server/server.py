import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request
from flask import send_from_directory
from blockchain import *
from crossdomain import *
import json

import data

import pyqrcode
import io
import uuid
import traceback

# Instantiate the app
app = Flask(__name__)

REQUIRED = ['vendor', 'produce', 'quantity', 'date']

def obj2array(values):
  if not all(k in values for k in REQUIRED):
    return 'Missing values', 400
  vendor = values['vendor']
  return [values[n] for n in REQUIRED]

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)


@app.route('/sign', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
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
  qrimg = pyqrcode.create(sign.decode(), error='L', version=27, mode='binary')
  fn = str(uuid.uuid1())
  qrimg.svg('images/{}.svg'.format(fn), scale=8)
  response = {'signature': sign.decode(),
      'svg': 'images/{}.svg'.format(fn)
      }
  return jsonify(response), 201

@app.route('/verify', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def verify():
  jj = request.get_json()
  if isinstance(jj, str):
    values = json.loads(request.get_json())
  else:
    values = jj
  required =  ['signature'] + ['vendor', 'produce', 'quantity', 'date']
  if not all(k in values for k in required):
    return 'Missing values', 400
  vendor = values['vendor']
  signature = values['signature']
  obj = obj2array(values)

  (res, msg) = verify_block_data(vendor, obj, signature)
  response = {'result': res, 'message': msg }
  return jsonify(response), 201

def server_wrapper(fn):
  try:
    jj = request.get_json()
    if isinstance(jj, str):
      values = json.loads(request.get_json())
    else:
      values = jj
    rr = fn(**values)
    return jsonify(rr), 201
  except Exception as e:
    print('print_exc():')
    traceback.print_exc()
    print('Exception: {}'.format(str(e)))
    return jsonify({'error': str(e)}), 404

@app.route('/vendorid', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def get_vendor_id():
  return server_wrapper(data.get_vendor_id)


@app.route('/vendors', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def get_all_vendors():
  return server_wrapper(data.get_all_vendors)


@app.route('/holds', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def get_holds():
  return server_wrapper(data.get_holds)

@app.route('/pendings', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def get_pendings():
  return server_wrapper(data.get_pendings)

@app.route('/transhistory', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def get_trans_history():
  return server_wrapper(data.get_trans_history)

@app.route('/addtrans', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def add_trans():
  return server_wrapper(data.add_trans_encrypt)

@app.route('/confirmtrans', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def confirm_trans():
  return server_wrapper(data.confirm_trans_decrypt)

@app.route('/encrdata', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers="Content-Type, Access-Control-Allow-Headers")
def get_encrypt_data():
  return server_wrapper(data.get_encrypt_data)




if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
  args = parser.parse_args()
  port = args.port

  app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
