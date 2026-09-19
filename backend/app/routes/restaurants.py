from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_role
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    new_restaurant = Restaurant(
        owner_id=current_user.id,
        name=data.name,
        description=data.description,
        cusine_type=data.cusine_type,
        address=data.address,
        phone=data.phone,
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

@router.get("/", response_model=list[RestaurantResponse])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()
