from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from app.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"),nullable=False )
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Numeric(10,2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    image_url = Column(String(500), nullable=True)