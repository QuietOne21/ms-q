from sqlalchemy import Column, Integer, String,  Date, Time, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class ReservationStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    no_show = "no_show"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"), nullable=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    party_size = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.pending)
    special_requests = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())