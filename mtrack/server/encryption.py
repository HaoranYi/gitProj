from Crypto.PublicKey import RSA
from model import Vendor
import hashlib

def gen_signature(obj):
  m = hashlib.sha256()
  for x in obj:
    m.update(str(x).encode())
  return m.digest()

def encrypt(vendor, obj):
  key = RSA.importKey(vendor.pubkey)
  sig = gen_signature(obj)
  return key.encrypt(vendor.uniqid.encode() + sig, 32)

def decrypt(vendor, obj):
  key = RSA.importKey(vendor.prvkey)
  r = key.decrypt(obj)
  return (r[:32], r[32:])

def encrypt_s(vendor, s='mysecret'):
  key = RSA.importKey(vendor.pubkey)
  return key.encrypt(vendor.uniqid.encode() + s, 32)
