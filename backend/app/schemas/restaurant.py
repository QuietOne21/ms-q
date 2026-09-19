from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cusine_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class RestaurantResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str]
    cusine_type: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True