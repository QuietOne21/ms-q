from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_role
from app.models.user import User, UserRole
from app.models.restaurant_table import RestaurantTable
from app.schemas.restaurant_table import TableCreate, TableResponse
from app.routes.restaurants import get_owned_restaurant

router = APIRouter(prefix="/restaurants/{restaurant_id}/tables", tags=["tables"])

@router.post("/", response_model=TableResponse)
def create_table(
    restaurant_id: int,
    data: TableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    get_owned_restaurant(restaurant_id, current_user, db)

    new_table = RestaurantTable(restaurant_id=restaurant_id, label=data.label, seats=data.seats)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.get("/", response_model=list[TableResponse])
def list_tables(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(RestaurantTable).filter(RestaurantTable.restaurant_id == restaurant_id).all()

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    restaurant_id: int,
    table_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.res_admin)),
):
    get_owned_restaurant(restaurant_id, current_user, db)

    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == table_id,
        RestaurantTable.restaurant_id == restaurant_id,
    ).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    db.delete(table)
    db.commit()