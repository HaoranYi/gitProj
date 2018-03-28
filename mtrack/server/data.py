from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Vendor

def get_vendor(name):
  try:
    engine = create_engine('sqlite:///vendor.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Vendor).filter(Vendor.name == name).one()
  except Exception as e:
    print('can not find vendor {}'.format(name))
    return None
  finally:
    session.close()
    engine.dispose()
