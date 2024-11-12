from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, extract, or_
from datetime import date, timedelta

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate

async def get_contacts(skip: int, limit: int, db: AsyncSession) -> List[Contact]:
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()

async def get_contact(db: AsyncSession, contact_id: Optional[int] = None, name: Optional[str] = None, surname: Optional[str] = None, email: Optional[str] = None) -> List[Contact]:
    if contact_id:
        result = await db.execute(select(Contact).filter(Contact.id == contact_id))
        return result.scalars().all()
    if name:
        result = await db.execute(select(Contact).filter(Contact.name == name))
        return result.scalars().all()
    if surname:
        result = await db.execute(select(Contact).filter(Contact.surname == surname))
        return result.scalars().all()
    if email:
        result = await db.execute(select(Contact).filter(Contact.email == email))
        return result.scalars().all()
    return []

async def create_contact(contact: ContactCreate, db: AsyncSession) -> Contact:
    new_contact = Contact(
        name=contact.name, surname=contact.surname, email=contact.email,
        phone=contact.phone, birthday=contact.birthday
    )
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact

async def update_contact(contact_id: int, contact: ContactUpdate, db: AsyncSession) -> Optional[Contact]:
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    db_contact = result.scalar_one_or_none()
    if db_contact:
        db_contact.name = contact.name
        db_contact.surname = contact.surname
        db_contact.email = contact.email
        db_contact.phone = contact.phone
        db_contact.birthday = contact.birthday
        await db.commit()
        await db.refresh(db_contact)
    return db_contact

async def delete_contact(contact_id: int, db: AsyncSession) -> Optional[Contact]:
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    db_contact = result.scalar_one_or_none()
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
    return db_contact

async def get_upcoming_birthdays(db: AsyncSession) -> List[Contact]:
    today = date.today()
    end_date = today + timedelta(days=7)
    
    query = select(Contact).filter(
        or_(
            and_(
                extract('month', Contact.birthday) == today.month,
                extract('day', Contact.birthday) >= today.day,
                extract('day', Contact.birthday) <= end_date.day
            ),
            and_(
                extract('month', Contact.birthday) == end_date.month,
                extract('day', Contact.birthday) <= end_date.day
            )
        )
    )
    
    result = await db.execute(query)
    return result.scalars().all()