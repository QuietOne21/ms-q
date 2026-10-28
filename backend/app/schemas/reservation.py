from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional
from app.models.reservation import ReservationStatus

class ReservationCreate(BaseModel):
    restaurant_id: int
    date: date
    time: time
    party_size: int = Field(gt=0, le=20)
    special_requests: Optional[str] = Field(default=None, max_length=1000)

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