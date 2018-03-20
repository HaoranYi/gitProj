from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Vendor

engine = create_engine('sqlite:///vendor.db', echo=False)
Session = sessionmaker(bind=engine)

def get_vendor(name):
  try:
    return Session().query(Vendor).filter(Vendor.name == name).one()
  except Exception as e:
    print('can not find vendor {}'.format(name))
    return None





