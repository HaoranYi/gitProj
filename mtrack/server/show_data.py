from sqlalchemy import create_engine
from model import Base, Vendor, Medicine, Transaction, Hold
from trans_state import TransState

from sqlalchemy.orm import sessionmaker
from key_gen import generate
import datetime
import uuid

## create a database of vendors

engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# check
print('=====Vendor=====')
for x in session.query(Vendor).order_by(Vendor.id):
  print(x)
  print(x.buy_transactions)
  print(x.sell_transactions)
  print(x.holds)

print('=====Medicine=====')
for x in session.query(Medicine).order_by(Medicine.id):
  print(x)
  print(x.transactions)
  print(x.holds)

print('=====Transaction=====')
for x in session.query(Transaction).order_by(Transaction.id).limit(5):
  print(x)
  print(x.buyer)
  print(x.seller)
  print(x.medicine)

print('=====Holds=====')
for x in session.query(Hold).limit(5):
  print(x)


