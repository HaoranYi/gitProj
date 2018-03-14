from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///vendor.db', echo=True)
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime

class Vendor(Base):
    __tablename__ = 'tbVendors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    uniqid = Column(String)
    pubkey = Column(String)
    created = Column(DateTime)

    def __repr__(self): 
        return "<vendor(name='%s', uniqid='%s', pubkey='%s')>" % (self.name, 
                self.uniqid, self.pubkey) 


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
import datetime
import uuid
Session = sessionmaker(bind=engine)

v = Vendor(name='BBB', uniqid=uuid.uuid4().hex, pubkey='key',
        created=datetime.datetime.now())
session = Session()
session.add(v)
session.commit()
        
for x in session.query(Vendor).order_by(Vendor.id):
    print(x)
