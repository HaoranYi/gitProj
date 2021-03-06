from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Vendor, Medicine, Transaction, Hold
import datetime
from trans_state import TransState
import encryption
import random
import binascii


DB = 'sqlite:///database.db'

def get_vendor(name):
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Vendor).filter(Vendor.name == name).one()
  except Exception as e:
    print('can not find vendor {}'.format(name))
    return None
  finally:
    session.close()
    engine.dispose()


def get_vendor_id(name):
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Vendor).filter(Vendor.name == name).one().id
  except Exception as e:
    print('can not find vendor {}'.format(name))
    return None
  finally:
    session.close()
    engine.dispose()


def get_all_vendors():
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return [name[0] for name in session.query(Vendor.name)]
  except Exception as e:
    print('Exception:{}'.format(e))
    return None
  finally:
    session.close()
    engine.dispose()


def get_holds(name):
  """ return the items that vendor holds (including pending sales)

  Args:
    name(str): vendor name
  Returns:
    list
  """
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return [{"name":x.medicine.name, "m_id":x.medicine.id, "pending":x.is_pending} for x in session.query(Vendor).filter(Vendor.name == name).one().holds]
  except Exception as e:
    print('Exception:{}'.format(e))
    return None
  finally:
    session.close()
    engine.dispose()

def get_pendings(name):
  """ return the items that vendor's buyer confirmation

  Args:
    name(str): vendor name
  """
  try:
    engine = create_engine(DB, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return [{'id':h.id, 'name': h.medicine.name, 'm_id':h.medicine.id} for (v, h, t) in session.query(Vendor, Hold, Transaction).\
                      filter(Vendor.name == name).\
                      filter(Vendor.id == Transaction.buyer_id).\
                      filter(Hold.holder_id == Transaction.seller_id).\
                      filter(Hold.is_pending == True).\
                      filter(Hold.last_trans_id == Transaction.id).\
                      all()]
  except Exception as e:
    print('can not find vendor {}'.format(name))
    return None
  finally:
    session.close()
    engine.dispose()

def get_trans_history(medicine_id):
  """ return the history for transactions for a hold

  Args:
    hold_id(int): hold id (tbHolds)
  Returns:
    list
  """
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return [{
        'id': t.id,
        'name':t.medicine.name,
        'buyer':t.buyer.name,
        'seller':t.seller.name,
        'date':t.created,
        'pending': t.state == TransState.PENDING.value,
        'secret': t.secret if isinstance(t.secret, str) else t.secret.decode(),
        } for t in session.query(Transaction).\
                      filter(medicine_id == Transaction.medicine_id).\
                      order_by(Transaction.id.desc()).\
                      all()]
  except Exception as e:
    print('Exception: {}'.format(e))
    return None
  finally:
    session.close()
    engine.dispose()



def get_medicine(name):
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Medicine).filter(Medicine.name == name).one()
  except Exception as e:
    print('can not find medicine {}'.format(name))
    return None
  finally:
    session.close()
    engine.dispose()

def add_trans(hold_id, buyer_id):
  """ Add a new transction for the hold

  Args:
    hold_id(int): hold id (tbHolds)
    buyer_id(int): buyer id (tbVendors)

  Returns:
    boolean
  """
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    hold = session.query(Hold).filter(Hold.id == hold_id).one()
    seller = session.query(Vendor).filter(Vendor.id == buyer_id).one()
    if hold.is_pending:
      raise Exception('pending transactions.')
    if buyer_id == hold.holder_id:
      raise Exception('same buyer and seller.')
    # Add transaction
    hold.last_trans = Transaction(medicine_id=hold.medicine_id, seller_id=hold.holder_id, buyer_id=buyer_id,
          created=datetime.datetime.now(), last_update=datetime.datetime.now(),
          state=TransState.PENDING.value , parent_trans_id=hold.last_trans_id)
    hold.is_pending = True
    session.commit()
    return {'result':True}
  except Exception as e:
    print('exeption: {}'.format(e))
    raise e
  finally:
    session.close()
    engine.dispose()

def confirm_trans(hold_id):
  """ Confirm a pending sale (update both tbTransactions and tbHolds)

  Args:
    hold_id(int): hold id (tbHolds)
  Returns:
    boolean
  """
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    hold = session.query(Hold).filter(Hold.id == hold_id).one()
    if not hold.is_pending:
      raise Exception('not a pending transactions.')
    # Add transaction
    hold.last_trans.state = TransState.CONFIRMED
    hold.last_trans.last_update = datetime.datetime.now()
    hold.holder_id = hold.last_trans.buyer_id
    hold.is_pending = False
    session.commit()
    return {'result':True}
  except Exception as e:
    print('exeption:{}'.format(e))
    raise e
  finally:
    session.close()
    engine.dispose()

## encryption

def add_trans_encrypt(hold_id, buyer_id):
  """ Add a new transction for the hold

  Args:
    hold_id(int): hold id (tbHolds)
    buyer_id(int): buyer id (tbVendors)

  Returns:
    boolean
  """
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    hold = session.query(Hold).filter(Hold.id == hold_id).one()
    seller = session.query(Vendor).filter(Vendor.id == buyer_id).one()
    secret = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5))
    enc_data = encryption.encrypt_s(seller, secret.encode())
    if hold.is_pending:
      raise Exception('pending transactions.')
    if buyer_id == hold.holder_id:
      raise Exception('same buyer and seller.')
    # Add transaction
    hold.last_trans = Transaction(medicine_id=hold.medicine_id, seller_id=hold.holder_id, buyer_id=buyer_id,
          created=datetime.datetime.now(), last_update=datetime.datetime.now(),
          state=TransState.PENDING.value , parent_trans_id=hold.last_trans_id,
          secret=secret.encode())
    hold.is_pending = True
    hold.enc_data = b''.join(enc_data)
    session.commit()
    return {'result':True}
  except Exception as e:
    print('exeption: {}'.format(e))
    raise e
  finally:
    session.close()
    engine.dispose()



def confirm_trans_decrypt(hold_id, data=None):
  """ Confirm a pending sale (update both tbTransactions and tbHolds)

  Args:
    hold_id(int): hold id (tbHolds)
  Returns:
    boolean
  """
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    hold = session.query(Hold).filter(Hold.id == hold_id).one()
    if not hold.is_pending:
      raise Exception('not a pending transactions.')

    buyer = hold.last_trans.buyer
    if not data:
      enc_data = hold.enc_data
    else:
      enc_data = binascii.unhexlify(data)
    (r1, r2) = encryption.decrypt(buyer, enc_data)
    if r1 != buyer.uniqid.encode():
      print(r1, buyer.uniqid.encode())
      raise Exception('unmatched buyer id')
    if r2 != hold.last_trans.secret:
      print(r2, hold.last_trans.secret)
      raise Exception('unmatched secret')
    # Add transaction
    hold.last_trans.state = TransState.CONFIRMED
    hold.last_trans.last_update = datetime.datetime.now()
    hold.holder_id = hold.last_trans.buyer_id
    hold.is_pending = False
    session.commit()
    return {'result':True}
  except Exception as e:
    print('exeption:{0}'.format(e))
    raise e
  finally:
    session.close()
    engine.dispose()

def get_encrypt_data(hold_id):
  try:
    engine = create_engine(DB, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    hold = session.query(Hold).filter(Hold.id == hold_id).one()
    return { 'data': binascii.hexlify(hold.enc_data).decode() }
  except Exception as e:
    print('exeption:{0}'.format(e))
    raise e
  finally:
    session.close()
    engine.dispose()


