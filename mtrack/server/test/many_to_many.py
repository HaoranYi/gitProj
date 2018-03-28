## many-to-many relationship
ItemDetail = Table('ItemDetail',
    Column('id', Integer, primary_key=True),
    Column('itemId', Integer, ForeignKey('Item.id')),
    Column('detailId', Integer, ForeignKey('Detail.id')),
    Column('endDate', Date))

class Item(Base):
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    details = relationship('Detail', secondary=ItemDetail, backref='Item')

class Detail(Base):
    __tablename__ = 'Detail'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    items = relationship('Item', secondary=ItemDetail, backref='Detail')


## one-to-many relationship
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship("Address", back_populates='user',
                    cascade="all, delete, delete-orphan")

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                               self.name, self.fullname, self.password)



class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address
