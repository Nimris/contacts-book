from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date)
    