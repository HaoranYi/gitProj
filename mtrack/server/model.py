from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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

  buy_transactions = relationship("Transaction", foreign_keys="Transaction.buyer_id", back_populates='buyer')
  sell_transactions = relationship("Transaction", foreign_keys="Transaction.seller_id", back_populates='seller')
  holds = relationship("Hold", order_by="Hold.id.desc()", back_populates='holder')


  def __repr__(self):
    return "<vendor(name='%s', uniqid='%s', pubkey='%s')>" % (self.name,
        self.uniqid, self.pubkey)


class Medicine(Base):
  __tablename__ = 'tbMedicines'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  created = Column(DateTime)

  transactions = relationship("Transaction", order_by="Transaction.id.desc()",
      back_populates='medicine')
  holds = relationship("Hold", order_by="Hold.id.desc()",
      back_populates='medicine')

  def __repr__(self):
    return "<medicine(name='%s', id='%d', created='%s')>" % (self.name,
        self.id, str(self.created))


class Transaction(Base):
  __tablename__ = 'tbTransactions'
  id = Column(Integer, primary_key=True)
  medicine_id = Column(Integer, ForeignKey('tbMedicines.id'))
  seller_id = Column(Integer, ForeignKey('tbVendors.id'))
  buyer_id = Column(Integer, ForeignKey('tbVendors.id'))
  created = Column(DateTime)
  last_update = Column(DateTime)
  state = Column(Integer)  ## see TransState (trans_state.py)
  parent_trans_id = Column(Integer)

  seller = relationship("Vendor", foreign_keys="Transaction.seller_id", back_populates='sell_transactions')
  buyer = relationship("Vendor", foreign_keys="Transaction.buyer_id", back_populates='buy_transactions')
  medicine = relationship("Medicine", back_populates='transactions')

  def __repr__(self):
    return "<transaction(id='%d', medicine_id='%d', buyer_id='%d',"       \
      "seller_id=%d, careted=%s, laste_updated=%s, state=%s, parent_trans_id=%d)>" %(self.id, \
          self.medicine_id, self.buyer_id, self.seller_id, self.created,  \
          self.last_update, self.state, self.parent_trans_id)

class Hold(Base):
  __tablename__ = 'tbHolds'

  id = Column(Integer, primary_key=True)
  medicine_id = Column(Integer, ForeignKey('tbMedicines.id'))
  holder_id = Column(Integer, ForeignKey('tbVendors.id'))
  last_trans_id = Column(Integer, ForeignKey('tbTransactions.id'))
  #created = Column(DateTime)
  #last_update = Column(DateTime)
  is_pending = Column(Boolean)

  last_trans = relationship("Transaction")
  medicine = relationship("Medicine", back_populates='holds')
  holder = relationship("Vendor")

  def __repr__(self):
    return "<hold(medicine='%s', holder='%s', last_trans='%d', is_pending='%d')>" \
        % (self.medicine.name, self.holder.name, self.last_trans.id, self.is_pending)



