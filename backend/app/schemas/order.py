from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    reservation_id: int
    items: list[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price_at_time_of_order: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    reservation_id: int
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemResponse]
    total: Decimal

    class Config: from_attributes = True