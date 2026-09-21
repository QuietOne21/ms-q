from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_role
from app.models.user import User, UserRole
from app.models.menu_category import MenuCategory
from app.schemas.menu_category import MenuCategoryCreate, MenuCategoryResponse
from app.routes.restaurants import get_owned_restaurant

router = APIRouter(prefix="/restaurants/{restaurant_id}/categories", tags=["menu"])

@router.post("/", response_model=MenuCategoryResponse)
def create_category(
    restaurant_id: int,
    data: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    get_owned_restaurant(restaurant_id, current_user, db)

    category = MenuCategory(restaurant_id=restaurant_id, name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/", response_model=list[MenuCategoryResponse])
def list_categories(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(MenuCategory).filter(MenuCategory.restaurant_id == restaurant_id).all()

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    restaurant_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    get_owned_restaurant(restaurant_id, current_user, db)

    category = db.query(MenuCategory).filter(
        MenuCategory.id == category_id,
        MenuCategory.restaurant_id == restaurant_id,
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()