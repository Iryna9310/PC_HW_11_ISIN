from pydantic import BaseModel
from datetime import date
from typing import Optional

# Базовий клас Contact для Pydantic
class ContactBase(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str
    birthday: date

# Клас для створення нового контакту
class ContactCreate(ContactBase):
    pass

# Клас для оновлення існуючого контакту
class ContactUpdate(ContactBase):
    pass

# Клас для представлення контакту з ID
class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True




