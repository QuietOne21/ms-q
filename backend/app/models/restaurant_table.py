from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    label = Column(String(50), nullable=False)
    seats = Column(Integer, nullable=False)