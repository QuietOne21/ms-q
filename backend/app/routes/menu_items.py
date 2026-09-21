from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_role
from app.models.user import User, UserRole
from app.models.menu_item import MenuItem
from app.models.menu_category import MenuCategory
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse
from app.routes.restaurants import get_owned_restaurant

router = APIRouter(prefix="/restaurants/{restaurant_id}/items", tags=["menu"])

def get_valid_category(category_id: int, restaurant_id: int, db: Session) -> MenuCategory:
    category = db.query(MenuCategory).filter(
        MenuCategory.id == category_id,
        MenuCategory.restaurant_id == restaurant_id,
    ).first()

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category does not exist or does not belong to this restaurant",
        )
    return category

@router.post("/", response_model=MenuItemResponse)
def create_item(
    restaurant_id: int,
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    get_owned_restaurant(restaurant_id, current_user, db)
    get_valid_category(data.category_id, restaurant_id, db)

    item = MenuItem(
        restaurant_id=restaurant_id,
        category_id=data.category_id,
        name=data.name,
        description=data.description,
        price=data.price,
        image_url=data.image_url,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/", response_model=list[MenuItemResponse])
def list_items(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

@router.put("/{item_id}", response_model= MenuItemResponse)
def update_item(
    restaurant_id: int,
    item_id: int,
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):

    get_owned_restaurant(restaurant_id, current_user, db)
    get_valid_category(data.category_id, restaurant_id, db)

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id,
        MenuItem.restaurant_id == restaurant_id,
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    item.category_id = data.category_id
    item.name = data.name
    item.description = data.description
    item.price = data.price
    item.image_url = data.image_url

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    restaurant_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    get_owned_restaurant(restaurant_id, current_user, db)

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id,
        MenuItem.restaurant_id == restaurant_id,
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(item)
    db.commit()