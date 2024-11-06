from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    name: str = Field(max_length=50, example="John")
    surname: str = Field(max_length=50, example="Doe")
    email: str = Field(..., example="example@gmail.com")
    phone: str = Field(max_length=15, example="1234567890")
    birthday: Optional[datetime] = Field(None, example="2021-01-01")
    

class ContactUpdate(ContactBase):
    pass


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int
    
    class Config:
        orm_mode = True
    
    