from gino import Gino
from sqlalchemy import Column, String
from pgvector.sqlalchemy import Vector

db = Gino()

class Purchasers(db.Model):
    __tablename__ = 'purchasers'
    fdesc = Column(Vector(128), primary_key=True)
    namehash = Column(String)
    name = Column(String)
    phone_number = Column(String)
    payment_token = Column(String)

    def __repr__(self):
        return f'{self.__tablename__} fdesc={self.fdesc} namehash={self.namehash}'

