from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts')


@router.get("/all", response_model=List[ContactResponse])
async def get_contacts(skip:int = 0, limit:int = 50, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/", response_model=List[ContactResponse])
async def get_contact(db: Session = Depends(get_db), contact_id: Optional[int] = None, name: Optional[str] = None, surname: Optional[str] = None, email: Optional[str] = None):
    contact = await repository_contacts.get_contact(db, contact_id, name, surname, email)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# async def get_contact(contact_id: int, db: Session = Depends(get_db)):
#     contact = await repository_contacts.get_contact(contact_id, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(contact, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, contact, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/upcoming_birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(db)
    return contacts