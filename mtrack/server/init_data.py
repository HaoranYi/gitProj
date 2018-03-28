from sqlalchemy import create_engine
from model import Base, Vendor, Medicine, Transaction, Hold
from trans_state import TransState

from sqlalchemy.orm import sessionmaker
from key_gen import generate
import datetime
import uuid

## create a database
engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# clear
session.query(Transaction).delete()
session.query(Vendor).delete()
session.query(Medicine).delete()
session.query(Hold).delete()

# init vendors
for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:3]:
  (pk, pv) = generate(None, None, 'PEM', 1024)
  v = Vendor(name='Vendor_' + x, uniqid=uuid.uuid4().hex, pubkey=pk, prvkey=pv, created=datetime.datetime.now())
  session.add(v)
session.commit()

# init medicine
for x in 'abcdefghijklmnopqrstuvwxyz'[:3]:
  m = Medicine(name='Med_' + x*3, created=datetime.datetime.now())
  session.add(m)
session.commit()

# init transaction
vendors = [x for x in session.query(Vendor)]
buyers = vendors[:-1]
sellers = vendors[1:]

for m in session.query(Medicine):
  parent_id = -1
  for (v1, v2) in zip(buyers, sellers):
    t = Transaction(medicine_id=m.id, seller_id=v1.id, buyer_id=v2.id,
          created=datetime.datetime.now(), last_update=datetime.datetime.now(),
          state=TransState.CONFIRMED.value , parent_trans_id=parent_id)
    session.add(t)
    session.commit()
    parent_id = t.id
  h = Hold(medicine_id=m.id, holder_id=v2.id, last_trans_id=t.id, is_pending=False)
  session.add(h)

session.commit()

# check
for x in session.query(Vendor).order_by(Vendor.id):
  print(x)
  print(x.buy_transactions)
  print(x.sell_transactions)
  print(x.holds)

for x in session.query(Medicine).order_by(Medicine.id):
  print(x)
  print(x.transactions)
  print(x.holds)

for x in session.query(Transaction).order_by(Transaction.id).limit(5):
  print(x)
  print(x.buyer)
  print(x.seller)
  print(x.medicine)

for x in session.query(Hold).limit(5):
  print(x)



