from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class MenuItemCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
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