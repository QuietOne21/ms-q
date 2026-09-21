from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_role
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse

from fastapi import HTTPException, status

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

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


def get_owned_restaurant(restaurant_id: int, current_user: User, db: Session) -> Restaurant:
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this restaurant")
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    restaurant = get_owned_restaurant(restaurant_id, current_user, db)
    restaurant.name = data.name
    restaurant.description = data.description
    restaurant.cusine_type = data.cusine_type
    restaurant.address = data.address
    restaurant.phone = data.phone

    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
   restaurant = get_owned_restaurant(restaurant_id, current_user, db)

   db.delete(restaurant)
   db.commit()

