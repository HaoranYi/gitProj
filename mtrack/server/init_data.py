from sqlalchemy import create_engine
from model import Vendor

from sqlalchemy.orm import sessionmaker
from key_gen import generate
import datetime
import uuid

## create a database of vendors

engine = create_engine('sqlite:///vendor.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.query(Vendor).delete()
for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
  (pk, pv) = generate(None, None, 'PEM', 1024)
  v = Vendor(name=x*3, uniqid=uuid.uuid4().hex, pubkey=pk, prvkey=pv, created=datetime.datetime.now())
  session.add(v)

session.commit()

for x in session.query(Vendor).order_by(Vendor.id):
    print(x)
