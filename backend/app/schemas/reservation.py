from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional
from app.models.reservation import ReservationStatus

class ReservationCreate(BaseModel):
    restaurant_id: int
    date: date
    time: time
    party_size: int
    special_requests: Optional[str] = None

class ReservationResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    table_id: Optional[int]
    date: date
    time: time
    party_size: int
    status: ReservationStatus
    special_requests: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True