from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, database

app = FastAPI()

# Залежність для отримання сесії бази даних
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact API"}

# Створення нового контакту
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Читання всіх контактів з можливістю пошуку
@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
    search: Optional[str] = None
):
    query = db.query(models.Contact)
    if search:
        query = query.filter(models.Contact.name.ilike(f"%{search}%"))
    contacts = query.offset(skip).limit(limit).all()
    return contacts

# Читання контакту за ID
@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Оновлення контакту
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Видалення контакту
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}

# Отримання контактів з днями народження протягом наступних 7 днів
@app.get("/contacts/birthday/", response_model=List[schemas.Contact])
def upcoming_birthdays(db: Session = Depends(get_db)):
    # Логіка для отримання контактів з днями народження у наступні 7 днів
    pass

# Пошук контактів за ім'ям, прізвищем або електронною поштою
@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(
    query: Optional[str] = None, db: Session = Depends(get_db)
):
    # Логіка для пошуку контактів за ім'ям, прізвищем або електронною поштою
    pass

# Створення таблиць бази даних при старті додатку
@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)
