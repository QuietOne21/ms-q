from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class MenuItemCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None

class MenuItemResponse(BaseModel):
    id: int
    restaurant_id: int
    category_id: int
    name: str
    description: Optional[str]
    price: Decimal
    is_available: bool
    image_url: Optional[str]

    class Config:
        from_attributes = True