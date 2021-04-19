from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String



Base = declarative_base()

class MyGeniusTable(Base):
 __tablename__ = 'MyGeniusTable'

 id = Column(Integer, primary_key=True)
 name = Column(String(100))
 value = Column(String(100))

 def __init__(self, name, value):
  self.name = name
  self.value = value

 def __repr__(self):
  return "<Settings(%s, %s)>" % (self.name, self.value)
