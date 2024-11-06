from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactCreate, ContactResponse, ContactUpdate


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(contact: ContactCreate, db: Session) -> Contact:
    new_contact = Contact(name=contact.name, surname=contact.surname, email=contact.email, phone=contact.phone, birthday=contact.birthday)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_contact(contact_id: int, contact: ContactUpdate, db: Session) -> Contact | None:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db_contact.name = contact.name
        db_contact.surname = contact.surname
        db_contact.email = contact.email
        db_contact.phone = contact.phone
        db_contact.birthday = contact.birthday
        db.commit()
        db.refresh(db_contact)
    return db_contact


async def delete_contact(contact_id: int, db: Session) -> Contact | None:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
        