from encryption import *
from data import get_vendor
import datetime
import binascii

ERROR_MESSAGE = {
    'ERR_VENDOR': 'Incorrect vendor.',
    'ERR_DATA': 'Incorrect data'
    }


def gen_block_data(vendor_name, obj):
  vendor = get_vendor(vendor_name)
  if not vendor:
    return None
  enc_data = encrypt(vendor, obj)  # 128byte
  h = b''
  for x in enc_data:
    h += binascii.hexlify(x)
  return h

def verify_block_data(vendor_name, obj, dat):
  vendor = get_vendor(vendor_name)
  if not vendor:
    return None
  enc_data = (binascii.unhexlify(dat),)
  (uuid, sig)= decrypt(vendor, enc_data)
  if vendor.uniqid.encode() != uuid:
    return (False, ERROR_MESSAGE['ERR_VENDOR'])
  sig2 = gen_signature(obj)
  if sig != sig2:
    return (False, ERROR_MESSAGE['ERR_DATA'])
  return (True, 'OK')


