from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from app.models.payment import PaymentStatus

class PaymentCreate(BaseModel):
    reservation_id: int

class PaymentResponse(BaseModel):
    id: int
    reservation_id: int
    amount: Decimal
    status: PaymentStatus
    payment_reference: str | None
    created_at: datetime

    class Config:
        from_attributes = True