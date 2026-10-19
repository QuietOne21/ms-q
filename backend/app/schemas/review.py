from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    reservation_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=2000)

class ReviewResponse(BaseModel):
    id: int
    reservation_id: int
    customer_id: int
    restaurant_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class RatingSummary(BaseModel):
    restaurant_id: int
    average_rating: Optional[float]
    review_count: int