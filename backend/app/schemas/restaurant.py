from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cusine_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    reservation_fee: Decimal = Decimal("0.00")

class RestaurantResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str]
    cusine_type: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    reservation_fee: Decimal
    created_at: datetime

    class Config:
        from_attributes = True