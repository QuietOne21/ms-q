from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cusine_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    reservation_fee: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)

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