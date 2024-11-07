from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Base = declarative_base()

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"
    id = Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name = Mapped[str] = mapped_column(String, index=True)
    surname = Mapped[str] = mapped_column(String, index=True)
    email = Mapped[str] = mapped_column(String, unique=True, index=True)
    phone = Mapped[str] = mapped_column(String, index=True)
    birthday = Mapped[Date] = mapped_column(Date)
    