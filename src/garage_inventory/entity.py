from datetime import date

from pydantic import BaseModel


class NewItem(BaseModel):
    name: str
    description: str
    owner: str
    expiration_date: date
    shipping: str
    price: float


class Item(NewItem):
    id: int
