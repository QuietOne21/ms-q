from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    cusine_type = Column(String(1000))
    address = Column(String(50))
    phone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")