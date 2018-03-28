from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vendor(Base):
    __tablename__ = 'tbVendors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    uniqid = Column(String)
    pubkey = Column(String)
    prvkey = Column(String)
    created = Column(DateTime)

    def __repr__(self):
        return "<vendor(name='%s', uniqid='%s', pubkey='%s')>" % (self.name,
                self.uniqid, self.pubkey)



class Medicine(Base):
    __tablename__ = 'tbMedicine'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # TODO (hyi) ...


    def __repr__(self):
        return "<medicine(name='%s', uniqid='%s', pubkey='%s')>" % (self.name,
                self.uniqid, self.pubkey)


class Transaction(Base):
    __tablename__ = 'tbTransaction'
    id = Column(Integer, primary_key=True)
    # TODO (hyi) ...



    def __repr__(self):
        return "<transaction(name='%s', uniqid='%s', pubkey='%s')>" % (self.name,
                self.uniqid, self.pubkey)
